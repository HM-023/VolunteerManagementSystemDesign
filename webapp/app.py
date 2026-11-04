"""Transactional SQLite volunteer scheduling and resource-intent workspace."""
import json
import sqlite3
import uuid
from datetime import date
from webapp.runtime import Store, integer, now, text, serve

def skills(value):
    if not isinstance(value,str) or len(value)>400:raise ValueError('Skills must be a comma-separated string up to 400 characters')
    result=sorted({v.strip().casefold() for v in value.split(',') if v.strip()})
    if not result:raise ValueError('At least one skill is required')
    return result

class Workspace:
    def __init__(self,directory):
        self.store=Store(directory)
        with self.store.connect() as db:
            db.executescript("""CREATE TABLE IF NOT EXISTS volunteers(id TEXT PRIMARY KEY,name TEXT NOT NULL,skills TEXT NOT NULL,created TEXT NOT NULL);
              CREATE TABLE IF NOT EXISTS opportunities(id TEXT PRIMARY KEY,title TEXT NOT NULL,skill TEXT NOT NULL,capacity INTEGER NOT NULL CHECK(capacity>0),day TEXT NOT NULL,created TEXT NOT NULL);
              CREATE TABLE IF NOT EXISTS assignments(id TEXT PRIMARY KEY,volunteer_id TEXT NOT NULL REFERENCES volunteers(id) ON DELETE CASCADE,opportunity_id TEXT NOT NULL REFERENCES opportunities(id) ON DELETE CASCADE,created TEXT NOT NULL,UNIQUE(volunteer_id,opportunity_id));
              CREATE TABLE IF NOT EXISTS donations(id TEXT PRIMARY KEY,category TEXT NOT NULL,description TEXT NOT NULL,status TEXT NOT NULL,created TEXT NOT NULL);
              CREATE TABLE IF NOT EXISTS activity(id INTEGER PRIMARY KEY AUTOINCREMENT,at TEXT NOT NULL,event TEXT NOT NULL,details TEXT NOT NULL);""")
    def audit(self,db,event,details):db.execute('INSERT INTO activity(at,event,details) VALUES(?,?,?)',(now(),event,details))
    def state(self):
        with self.store.connect() as db:
            volunteers=[{**dict(r),'skills':json.loads(r['skills'])} for r in db.execute('SELECT * FROM volunteers ORDER BY created DESC,id')]
            opportunities=[dict(r) for r in db.execute('SELECT o.*,COUNT(a.id) AS assigned FROM opportunities o LEFT JOIN assignments a ON o.id=a.opportunity_id GROUP BY o.id ORDER BY day,title')]
            assignments=[dict(r) for r in db.execute('SELECT a.*,v.name AS volunteer,o.title AS opportunity,o.day FROM assignments a JOIN volunteers v ON a.volunteer_id=v.id JOIN opportunities o ON a.opportunity_id=o.id ORDER BY o.day,v.name')]
            donations=[dict(r) for r in db.execute('SELECT * FROM donations ORDER BY created DESC,id')]
            activity=[dict(r) for r in db.execute('SELECT * FROM activity ORDER BY id DESC LIMIT 40')]
        return {'kind':'volunteer','title':'Community Operations','subtitle':'Coordinate skills, plan opportunities and keep resource intents moving through a clear workflow.','category':'SOFTWARE & SYSTEMS','volunteers':volunteers,'opportunities':opportunities,'assignments':assignments,'donations':donations,'activity':activity}
    def add_volunteer(self,body):
        identifier=str(uuid.uuid4());name=text(body.get('name'),'Name or alias',100);s=skills(body.get('skills',''))
        with self.store.connect() as db:
            db.execute('INSERT INTO volunteers VALUES(?,?,?,?)',(identifier,name,json.dumps(s),now()));self.audit(db,'volunteer_added',name)
        return {'id':identifier}
    def add_opportunity(self,body):
        identifier=str(uuid.uuid4());title=text(body.get('title'),'Opportunity title',150);skill=text(body.get('skill'),'Required skill',80).casefold();capacity=integer(body.get('capacity'),'Capacity',1,1000)
        try: day=date.fromisoformat(body.get('day','')).isoformat()
        except (ValueError,TypeError):raise ValueError('Date must use YYYY-MM-DD') from None
        with self.store.connect() as db:
            db.execute('INSERT INTO opportunities VALUES(?,?,?,?,?,?)',(identifier,title,skill,capacity,day,now()));self.audit(db,'opportunity_added',title)
        return {'id':identifier}
    def assign(self,body):
        identifier=str(uuid.uuid4())
        with self.store.connect() as db:
            # Serialize competing assignments before checking capacity and availability.
            db.execute('BEGIN IMMEDIATE')
            v=db.execute('SELECT * FROM volunteers WHERE id=?',(body.get('volunteer_id'),)).fetchone()
            o=db.execute('SELECT * FROM opportunities WHERE id=?',(body.get('opportunity_id'),)).fetchone()
            if not v or not o:raise ValueError('Volunteer or opportunity not found')
            if o['skill'] not in json.loads(v['skills']):raise ValueError('Volunteer skills do not match this opportunity')
            if db.execute('SELECT COUNT(*) FROM assignments WHERE opportunity_id=?',(o['id'],)).fetchone()[0]>=o['capacity']:raise ValueError('Opportunity is at capacity')
            if db.execute('SELECT 1 FROM assignments a JOIN opportunities o ON a.opportunity_id=o.id WHERE a.volunteer_id=? AND o.day=?',(v['id'],o['day'])).fetchone():raise ValueError('Volunteer already has an assignment on this date')
            db.execute('INSERT INTO assignments VALUES(?,?,?,?)',(identifier,v['id'],o['id'],now()));self.audit(db,'volunteer_assigned',v['name']+' → '+o['title'])
        return {'id':identifier}
    def action(self,body):
        action=body.get('action')
        if action=='volunteer':return self.add_volunteer(body)
        if action=='opportunity':return self.add_opportunity(body)
        if action=='assign':return self.assign(body)
        if action=='donation':
            identifier=str(uuid.uuid4());category=text(body.get('category'),'Category',80);description=text(body.get('description'),'Description',1000)
            with self.store.connect() as db:
                db.execute('INSERT INTO donations VALUES(?,?,?,?,?)',(identifier,category,description,'pledged',now()));self.audit(db,'donation_recorded',category)
            return {'id':identifier}
        if action=='donation_status':
            transitions={'pledged':['received','withdrawn'],'received':['distributed'],'distributed':[],'withdrawn':[]}
            with self.store.connect() as db:
                db.execute('BEGIN IMMEDIATE');old=db.execute('SELECT * FROM donations WHERE id=?',(body.get('id'),)).fetchone()
                if not old:raise ValueError('Donation intent not found')
                status=body.get('status')
                if status not in transitions[old['status']]:raise ValueError('Invalid resource-intent transition')
                db.execute('UPDATE donations SET status=? WHERE id=?',(status,old['id']));self.audit(db,'donation_status_changed',old['category']+' → '+status)
            return {'ok':True}
        if action=='delete':
            table=body.get('kind')
            if table not in ['volunteers','opportunities','assignments','donations']:raise ValueError('Unknown record type')
            with self.store.connect() as db:
                n=db.execute(f'DELETE FROM {table} WHERE id=?',(body.get('id'),)).rowcount
                if not n:raise ValueError('Record not found')
                self.audit(db,'record_removed',table+' / '+str(body.get('id')))
            return {'ok':True}
        if action=='export':
            snapshot=self.state();snapshot.pop('activity')
            return {'snapshot':snapshot,'note':'Local data export; review aliases and descriptions before sharing. No payment processing is implemented.'}
        if action=='demo':
            state=self.state()
            if state['volunteers'] or state['opportunities'] or state['donations']:raise ValueError('Demo can only be added to an empty workspace')
            # Explicit user action seeds fictional aliases; no real personal information.
            self.add_volunteer({'name':'Volunteer Cedar','skills':'logistics, coordination'})
            self.add_volunteer({'name':'Volunteer Maple','skills':'teaching, coordination'})
            self.add_volunteer({'name':'Volunteer Willow','skills':'logistics, design'})
            self.add_opportunity({'title':'Community Supply Day','skill':'logistics','capacity':2,'day':date.today().isoformat()})
            self.add_opportunity({'title':'Learning Circle','skill':'teaching','capacity':3,'day':date.today().isoformat()})
            self.action({'action':'donation','category':'Learning materials','description':'Fictional intent: 12 reusable notebooks'})
            return {'ok':True}
        raise ValueError('Unknown action')

if __name__=='__main__':serve(Workspace,8105)

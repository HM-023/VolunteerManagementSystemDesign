import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from webapp.app import Workspace
class OperationsTests(unittest.TestCase):
    def setUp(self):self.tmp=tempfile.TemporaryDirectory();self.w=Workspace(self.tmp.name)
    def tearDown(self):self.tmp.cleanup()
    def person(self,name='Cedar',skills='logistics'):return self.w.action({'action':'volunteer','name':name,'skills':skills})['id']
    def event(self,title='Supply day',skill='logistics',capacity=1,day='2027-01-10'):return self.w.action({'action':'opportunity','title':title,'skill':skill,'capacity':capacity,'day':day})['id']
    def assign(self,v,o):return self.w.action({'action':'assign','volunteer_id':v,'opportunity_id':o})
    def test_matching_and_restart_persistence(self):
        v=self.person(skills='Logistics, Teaching');o=self.event();self.assign(v,o)
        s=Workspace(self.tmp.name).state();self.assertEqual(len(s['assignments']),1);self.assertEqual(s['opportunities'][0]['assigned'],1)
    def test_capacity_skill_and_double_booking_checks(self):
        v=self.person();o=self.event();self.assign(v,o)
        with self.assertRaises(ValueError):self.assign(self.person('Maple'),o)
        with self.assertRaises(ValueError):self.assign(v,self.event('Second',capacity=3))
        with self.assertRaises(ValueError):self.assign(self.person('Willow','design'),self.event('Third'))
    def test_transaction_prevents_overbooking_under_concurrency(self):
        a=self.person('A');b=self.person('B');o=self.event()
        def attempt(v):
            try:self.assign(v,o);return True
            except ValueError:return False
        with ThreadPoolExecutor(2) as executor:results=list(executor.map(attempt,[a,b]))
        self.assertEqual(sum(results),1);self.assertEqual(len(self.w.state()['assignments']),1)
    def test_deletion_cascades_assignments_and_keeps_audit(self):
        v=self.person();o=self.event();self.assign(v,o);self.w.action({'action':'delete','kind':'volunteers','id':v})
        s=self.w.state();self.assertEqual(s['assignments'],[]);self.assertEqual(s['opportunities'][0]['assigned'],0);self.assertTrue(s['activity'])
    def test_resource_transition_enforced(self):
        d=self.w.action({'action':'donation','category':'Books','description':'Fictional books'})['id']
        with self.assertRaises(ValueError):self.w.action({'action':'donation_status','id':d,'status':'distributed'})
        for status in ['received','distributed']:self.w.action({'action':'donation_status','id':d,'status':status})
        with self.assertRaises(ValueError):self.w.action({'action':'donation_status','id':d,'status':'pledged'})
    def test_rejects_invalid_data(self):
        with self.assertRaises(ValueError):self.person(skills=' , ')
        with self.assertRaises(ValueError):self.event(capacity=0)
        with self.assertRaises(ValueError):self.event(day='2027-02-30')
        with self.assertRaises(ValueError):self.w.action({'action':'delete','kind':'documents; DROP TABLE volunteers','id':'x'})

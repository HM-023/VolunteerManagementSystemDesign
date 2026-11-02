using System.ComponentModel;
using System.Drawing;
using System.Windows.Forms;

namespace VolunteerManagementPrototype;

internal static class Program
{
    [STAThread]
    private static void Main()
    {
        ApplicationConfiguration.Initialize();
        Application.Run(new Dashboard());
    }
}

internal sealed class Dashboard : Form
{
    private readonly BindingList<VolunteerEntry> volunteers = new();
    private readonly BindingList<DonationEntry> donations = new();

    public Dashboard()
    {
        Text = "Community Operations | UI Prototype";
        MinimumSize = new Size(750, 500);
        Size = new Size(950, 600);
        StartPosition = FormStartPosition.CenterScreen;
        Font = new Font("Segoe UI", 10);
        BackColor = Color.FromArgb(244, 247, 250);

        var heading = new Label { Text = "Community Operations", Dock = DockStyle.Top,
            Font = new Font("Segoe UI Semibold", 19, FontStyle.Bold), Height = 65,
            Padding = new Padding(20, 15, 0, 0) };
        var tabs = new TabControl { Dock = DockStyle.Fill, Padding = new Point(15, 8) };
        tabs.TabPages.Add(BuildVolunteerTab());
        tabs.TabPages.Add(BuildDonationTab());
        Controls.Add(tabs);
        Controls.Add(heading);
    }

    private TabPage BuildVolunteerTab()
    {
        var page = new TabPage("Volunteers") { Padding = new Padding(15) };
        var layout = CreateLayout();
        var name = CreateInput(0, "Volunteer name or alias:", layout);
        var interest = CreateInput(1, "Area of interest:", layout);
        var add = new Button { Text = "Add volunteer", Width = 165, Height = 36 };
        add.Click += (_, _) =>
        {
            if (string.IsNullOrWhiteSpace(name.Text) || string.IsNullOrWhiteSpace(interest.Text))
            { MessageBox.Show("Enter a name and interest before continuing.", "Missing data"); return; }
            volunteers.Add(new VolunteerEntry(name.Text.Trim(), interest.Text.Trim()));
            name.Clear(); interest.Clear(); name.Focus();
        };
        layout.Controls.Add(add, 1, 2);
        var grid = CreateGrid(volunteers);
        layout.Controls.Add(grid, 0, 3);
        layout.SetColumnSpan(grid, 2);
        page.Controls.Add(layout);
        return page;
    }

    private TabPage BuildDonationTab()
    {
        var page = new TabPage("Donation intents") { Padding = new Padding(15) };
        var layout = CreateLayout();
        var category = CreateInput(0, "Resource category:", layout);
        var description = CreateInput(1, "Brief description:", layout);
        var add = new Button { Text = "Add donation intent", Width = 175, Height = 36 };
        add.Click += (_, _) =>
        {
            if (string.IsNullOrWhiteSpace(category.Text) || string.IsNullOrWhiteSpace(description.Text))
            { MessageBox.Show("Enter a category and description before continuing.", "Missing data"); return; }
            donations.Add(new DonationEntry(category.Text.Trim(), description.Text.Trim()));
            category.Clear(); description.Clear(); category.Focus();
        };
        layout.Controls.Add(add, 1, 2);
        var grid = CreateGrid(donations);
        layout.Controls.Add(grid, 0, 3);
        layout.SetColumnSpan(grid, 2);
        page.Controls.Add(layout);
        return page;
    }

    private static TableLayoutPanel CreateLayout()
    {
        var layout = new TableLayoutPanel { Dock = DockStyle.Fill, ColumnCount = 2, RowCount = 4,
            AutoScroll = true, Padding = new Padding(5) };
        layout.ColumnStyles.Add(new ColumnStyle(SizeType.Absolute, 205));
        layout.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 100));
        layout.RowStyles.Add(new RowStyle(SizeType.Absolute, 56));
        layout.RowStyles.Add(new RowStyle(SizeType.Absolute, 56));
        layout.RowStyles.Add(new RowStyle(SizeType.Absolute, 58));
        layout.RowStyles.Add(new RowStyle(SizeType.Percent, 100));
        return layout;
    }

    private static TextBox CreateInput(int row, string caption, TableLayoutPanel layout)
    {
        layout.Controls.Add(new Label { Text = caption, Dock = DockStyle.Fill,
            TextAlign = ContentAlignment.MiddleLeft }, 0, row);
        var input = new TextBox { Dock = DockStyle.Fill, Margin = new Padding(5, 12, 5, 12), MaxLength = 120 };
        layout.Controls.Add(input, 1, row);
        return input;
    }

    private static DataGridView CreateGrid<T>(BindingList<T> source)
    {
        return new DataGridView { Dock = DockStyle.Fill, DataSource = source, AutoSizeColumnsMode =
            DataGridViewAutoSizeColumnsMode.Fill, ReadOnly = true, AllowUserToAddRows = false,
            AllowUserToDeleteRows = false, RowHeadersVisible = false, BackgroundColor = Color.White };
    }
}

internal sealed record VolunteerEntry(string NameOrAlias, string Interest);
internal sealed record DonationEntry(string Category, string Description);

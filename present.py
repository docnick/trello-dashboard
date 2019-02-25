import trello_metrics
import date_utils
from IPython.core.display import display, HTML


def css_table_formatting():
    display(HTML(
        """
        <style>
        .rendered_html table {
            width: 100%;
        }
        
        .rendered_html td, 
        .rendered_html th {
            text-align: center;
        }
        </style>
        """
    ))


def hide_code():
    display(HTML(
    """
    <script>
        code_show=true; 
        function code_toggle() {
         if (code_show){
            $('div.input').hide();
         } else {
            $('div.input').show();
         }
         code_show = !code_show
        } 
        $( document ).ready(code_toggle);
    </script>
    <form action="javascript:code_toggle()">
        <input type="submit" value="Click here to toggle on/off the raw code.">
    </form>
    """))


def print_oldest_cards(open_cards):
    old_cards = trello_metrics.get_x_oldest_cards(open_cards)
    print_cards(old_cards, ["Cards", "Days Old"])


def print_cards(card_tuples, colum_headers):
    display(HTML(
        """
        <table>
            <tr>
                <th><h2>{}</h2></th>
                <th><h2>{}</h2></th>
            </tr>
            <tr>
                {}
            </tr>
        </table>
        """.format(colum_headers[0], colum_headers[1], '</tr><tr>'.join(
                '<td>{}</td>'.format('</td><td>'.join([card.get('name'), str(x)])) for card, x in card_tuples)
        )
    ))


def create_today_tasks_table(tasks_due_today_count, closed_tasks_due_today_count, open_past_due_tasks_count):
    percent_done = 1.0 * closed_tasks_due_today_count / tasks_due_today_count
    html_table = """
    <table>
      <tr>
        <th colspan="3"><h1>Today's Tasks ({})</h1></th>
      </tr>
      <tr>
        <td><h2>Total tasks due</h2></td>
        <td><h2>Tasks completed</h2></td> 
        <td><h2><font color="red">Past Due</font></h2></td>
      </tr>
      <tr>
        <td><h2>{}</h2></td>
        <td><h2>{}</h2></td> 
        <td><h2><font color="red">{}</font></h2></td>  
      </tr>
      <tr>
        <td colspan="3"><h2>{:.0f}% Complete</h2></td>
      </tr>
    </table>
    """.format(str(date_utils.get_today_date()), tasks_due_today_count,
               closed_tasks_due_today_count,
               open_past_due_tasks_count,
               percent_done * 100.0)

    return html_table

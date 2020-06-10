% include('header.tpl')
<!-- Main content should go here-->

<h1>{{ page_name }}</h1>
<h2>{{ body }}<h2>
<br>

<h3>{{ instructions }}<h3>

<br>

<% if errors: %>
<div class="row">
      <div class="col-md-12">
      <table class="table">
            <th class="col-md-3 text-left">Error</th>

            <% for error in errors: %>
            <tr>
                <td class="col-md-1 text-left">
                  <b>{{ error }}</b>
                </td>
            </tr>
              % end
          </table>
      </div>
    </div>
    % include('footer.tpl')



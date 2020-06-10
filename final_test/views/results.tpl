% include('header.tpl')
<!-- Main content should go here-->

<h1>{{ page_name }}</h1>
<br>

    <div class="row">
      <div class="col-md-12">
        <% if recipes: %>
          <table class="table">
            <th class="col-md-3 text-left">Recipe Name</th>
            <th class="col-md-2 text-left"></th>
            <th class="col-md-2 text-left"></th>
            <th class="col-md-2 text-left"></th>
            <th class="col-md-2 text-left"></th>
            <% for recipe in recipes: %>
              <tr>
                <td class="col-md-3 text-left">
                  <b>{{ recipe[1] }}</b>
                </td>
                <td class="col-md-1 text-left">
                    <a href="/ve/{{ recipe[0] }}">View/Edit</a></td>
                <td class="col-md-1 text-left">
                    <a href="/delete/{{ recipe[0] }}">Delete</a></td>
                <td class="col-md-1 text-left">
                    <a href="/ings/{{ recipe[0] }}">Show ingredients</a></td>
                <td class="col-md-1 text-left">
                    <a href="/add_ing/{{ recipe[0] }}">Add new ingredient</a></td>
              </tr>
              % end
          </table>
      </div>
    </div>
    % include('footer.tpl')
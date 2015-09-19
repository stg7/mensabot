<!DOCTYPE html>
<html>
  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="author" content="Steve Göring">
  <head>
    <title>{{title}}</title>
    % include('templates/header.tpl')
  </head>

  <body>
      <div class="container">
        % include('templates/nav.tpl')

        <div class="row marketing">
          <div class="col-lg-6">
           <h4>{{mensa}} <small><a href="/api/mensa/{{mensaname}}"> [api]</a></small></h4>
           <ul>
             % for f in food.get("res", []):
                {{f}}
             % end
           </ul>
          </div>



        </div>

        % include('templates/footer.tpl')
      </div>

  </body>

</html>
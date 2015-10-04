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
           mensas:
           <ul>
             % for m in sorted(mensas.keys()):
              <li><a href="./mensa/{{mensas[m]}}" >{{m}}</a></li>
             % end
           </ul>
          </div>

          <div class="col-lg-6">
            actions:
            <ul>
              <li><a href="/subscribe">subscribe</a>
              </li>
              <li><a href="/unsubscribe">unsubscribe</a></li>
            </ul>
          </div>

        </div>

        % include('templates/footer.tpl')
      </div>

  </body>

</html>
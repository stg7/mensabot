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
          <h4>About</h4>
          MensaBot+ is the successor of a small prototype. The idea for MensaBot starts in my first working days.
          I was always annoyed that I don't know which meals the university canteen called 'mensa' was offering.
          <h4>Api</h4>
          It is possible to do api calls to MensaBot+,
          <ul>
            <li><a href="./api/mensa/weimar">weimar example</a></li>
          </ul>
          </div>

        </div>

        % include('templates/footer.tpl')
      </div>

  </body>

</html>
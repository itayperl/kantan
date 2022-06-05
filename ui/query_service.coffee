app.service 'queryService', ($http) ->
  this.lookup = (search_term) ->
    $http.get('https://kantan.itayperl.name:4000/' + search_term)

  return this

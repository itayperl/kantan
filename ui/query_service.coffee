app.service 'queryService', ($http) ->
  this.lookup = (search_term) ->
    $http.get('http://kantan.itayperl.name:4000/' + search_term)

  return this

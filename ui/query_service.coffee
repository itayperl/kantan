app.service 'queryService', ($http) ->
  this.lookup = (search_term) ->
    $http.get('http://10.0.0.58:4000/' + search_term)

  return this

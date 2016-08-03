app.service 'queryService', ($http) ->
  this.lookup = (search_term) ->
    $http.get('http://kantan.nonze.ro:4000/' + search_term)

  return this

app.service 'queryService', ($http) ->
  this.lookup = (search_term) ->
    $http.get('http://ec2-52-25-208-204.us-west-2.compute.amazonaws.com:4000/' + search_term)

  return this

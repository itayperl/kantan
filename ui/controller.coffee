window.app = angular.module('app', [])

app.filter 'escape', -> window.encodeURIComponent

app.controller 'main', ($scope, queryService) ->
  $scope.add = (rad) ->
    $scope.search_bar.insert(rad)

  $scope.status  = ''
  $scope.results = []

  $scope.search_submit = (term) ->
    $scope.status = 'Searching...'

    xhr = queryService.lookup(term)

    xhr.success (data, status) ->
      if status == 200
        $scope.status = 'Results:'
        $scope.results = data
      else
        $scope.status = 'Error!'

    xhr.error ->
      $scope.status = 'Error!'

    xhr.finally ->
      $scope.searching = False
      
  $scope.examples = [
    '[儿田]法',
    '[罒]す',
    '[乃]う',
    '[韭][火]',
    '飛び[]る',
  ]

  $scope.search_example = (str) ->
    $scope.search_bar.set(str)
    $scope.search_submit(str)

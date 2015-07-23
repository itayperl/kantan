window.app = angular.module('app', ['ngRoute'])

app.filter 'escape', -> window.encodeURIComponent

app.config ($routeProvider) ->
  $routeProvider.when('/:term?', {
    templateUrl: 'main.html',
    controller:  'main',
  })
  $routeProvider.otherwise({
    redirectTo: '/'
  })

app.controller 'main', ($scope, $routeParams, $location, queryService) ->
  $scope.add = (rad) ->
    $scope.search_bar.insert(rad)

  $scope.term    = $routeParams.term or ''
  $scope.status  = ''
  $scope.results = []

  $scope.search_submit = ->
    $location.path("/#{$scope.term}")
    
  search = (term) ->
    $scope.status = 'Searching...'

    xhr = queryService.lookup(term)

    xhr.success (data, status) ->
      $scope.status = 'Results:'
      $scope.results = data

    xhr.error ->
      $scope.status = 'Error!'
      
  if $scope.term then search($scope.term)

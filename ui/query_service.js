// Generated by CoffeeScript 1.12.7
(function() {
  app.service('queryService', function($http) {
    this.lookup = function(search_term) {
      return $http.get('http://kantan.itayperl.name:4000/' + search_term);
    };
    return this;
  });

}).call(this);
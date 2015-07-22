// Generated by CoffeeScript 1.4.0
(function() {

  app.directive('searchBar', function() {
    return {
      restrict: 'E',
      templateUrl: 'search_bar.html',
      scope: {
        submit: '&',
        api: '='
      },
      controller: function($scope, $timeout) {
        var insert;
        insert = function(str, offset) {
          var post, pre;
          pre = $scope.text.substring(0, $scope.caret);
          post = $scope.text.substring($scope.caret, $scope.text.length);
          if (!/\[[^\]]*$/.test(pre)) {
            str = "[" + str + "]";
            offset -= 1;
          }
          $scope.text = pre + str + post;
          return $scope.caret += str.length + offset;
        };
        $scope.onSubmit = function() {
          return $timeout((function() {
            return $scope.submit({
              val: $scope.text
            });
          }), 300);
        };
        $scope.api = {
          insert: function(str) {
            return insert(str, 0);
          },
          set: function(str) {
            $scope.text = str;
            return $scope.caret = str.length;
          }
        };
        return $scope.text = '';
      }
    };
  });

  app.directive('trackCaret', function($timeout) {
    var getCursorPos, setCursorPos;
    getCursorPos = function(el) {
      var range;
      if (!(el.selectionStart != null)) {
        el.focus();
        range = document.selection.createRange();
        range.moveStart('character', -el.value.length);
        return range.text.length;
      } else {
        return el.selectionStart;
      }
    };
    setCursorPos = function(el, pos) {
      var range;
      if (!(el.selectionStart != null)) {
        el.focus();
        range = document.selection.createRange();
        range.moveStart('character', -el.value.length);
        range.moveStart('character', pos);
        range.moveEnd('character', 0);
        return range.select();
      } else {
        return el.selectionStart = el.selectionEnd = pos;
      }
    };
    return {
      require: 'ngModel',
      scope: {
        caret: '=trackCaret',
        model: '=ngModel'
      },
      link: function(scope, element, attrs, ctrl) {
        var old_render;
        scope.caret = 0;
        old_render = ctrl.$render;
        ctrl.$render = function() {
          old_render();
          return setCursorPos(element[0], scope.caret);
        };
        scope.$watch((function() {
          return getCursorPos(element[0]);
        }), (function(newVal) {
          return scope.caret = newVal;
        }));
        element.on('keyup mouseup keydown', function() {
          return $timeout(function() {
            return scope.$apply();
          });
        });
        return scope.$watch('model', (function(newVal) {
          return $timeout(function() {
            return scope.$digest();
          });
        }));
      }
    };
  });

  app.directive('keepFocus', function() {
    return {
      require: 'ngModel',
      link: function(scope, element, attrs, ctrl) {
        return element.on('blur', function() {
          return element[0].focus();
        });
      }
    };
  });

}).call(this);

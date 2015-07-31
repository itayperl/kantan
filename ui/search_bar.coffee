app.directive 'searchBar', ->
  return {
    restrict: 'E',
    templateUrl: 'search_bar.html',
    scope: { submit: '&', api: '=', text: '=value' }
    controller: ($scope, $timeout) ->
      insert = (str, offset) ->
        pre  = $scope.text.substring(0, $scope.caret)
        post = $scope.text.substring($scope.caret, $scope.text.length)

        if not /\[[^\]]*$/.test(pre)
          str = "[#{str}]"
          offset -= 1

        $scope.text   = pre + str + post
        $scope.caret += str.length + offset

      $scope.onSubmit = ->
        # wait 300ms to compensate for click delay: when entering a readical
        # and pressing enter quickly, the submit event fires before the click event
        $timeout( (-> $scope.submit(val: $scope.text) ), 300 )

      $scope.api = {
        insert: (str) -> insert(str, 0)
      }

      $scope.caret = $scope.text.length
  }

app.directive 'trackCaret', ($timeout) ->

  getCursorPos = (el) ->
    if not el.selectionStart?
      el.focus()
      range = document.selection.createRange()
      range.moveStart('character', -el.value.length)
      return range.text.length
    else
      return el.selectionStart

  setCursorPos = (el, pos) ->
    if not el.selectionStart?
      el.focus()
      range = document.selection.createRange()
      range.moveStart('character', -el.value.length)
      range.moveStart('character', pos)
      range.moveEnd('character', 0)
      range.select()
    else
      el.selectionStart = el.selectionEnd = pos

  return {
    require: 'ngModel',
    scope: {
      caret: '=trackCaret',
      model: '=ngModel',
    },
    link: (scope, element, attrs, ctrl) ->
      # update caret after every render
      old_render = ctrl.$render
      ctrl.$render = ->
        old_render()
        setCursorPos(element[0], scope.caret)

      # watch caret
      scope.$watch( (-> getCursorPos(element[0])), ((newVal) -> scope.caret = newVal) )

      # update caret (this combination seems to work)
      element.on('keyup mouseup keydown', -> $timeout(-> scope.$apply()) )

      # fixes caret not updating with japanese input method, after converting from kana
      scope.$watch('model', ((newVal) -> $timeout(-> scope.$digest()) ))
  }

app.directive 'keepFocus', ($timeout) ->

  return {
    require: 'ngModel',
    link: (scope, element, attrs, ctrl) ->
      $timeout -> element[0].focus()

      element.on 'blur', ->
        $timeout ->
          # keep focus but don't scroll into view
          [x, y] = [window.scrollX, window.scrollY]
          element[0].focus()
          window.scrollTo(x, y)
  }

/**
  Pulldown menu
  
  Usage:

    <!-- Pulldown directive is a custom HTML element.
         - Attribute pulldown-model creates an object in the parent scope with that name.
    -->
    <pulldown pulldown-model='myMenuPulldown'>

      <!-- Floating menu is anchored to the box containing these elements -->
      <pulldown-anchor>

        <!-- Object in $scope[pulldown-model] is used to expand and collapse the pulldown -->
        <button ng-click='myMenuPulldown.toggle()'>
          {{ myMenuPulldown.expanded ? '+' : '-' }}
          Menu
        </button>

      </pulldown-anchor>

      <!-- Everything in this element is shown in the pulldown.
           - style=right:0 right-aligns the pane (default is left-aligned)
           - style=min-width:* overrides the default minimum width of 100% relative to <pulldown>
      -->
      <pulldown-pane style='right:0; min-width:300px;'>
        <button>Menu</button>
      </pulldown-pane>

    </pulldown>

  CSS Notes:

  By default, the pulldown wrapper uses the default CSS display value of "inline",
  making the pulldown-pane as wide as the parent element, not the content inside
  pulldown-anchor. It also breaks alignment. It looks wonky, but it allows content
  inside pulldown-anchor to have width:100%

  To get the pulldown to pay attention to the pulldown-anchor's width and position,
  just set display:inline-block in <pulldown>

 */
app.directive('pulldown', function(LIB_ROOT) {
  return {
    restrict: 'E',
    transclude: {
      'anchor': 'pulldownAnchor',
      'pane':   'pulldownPane',
    },
    scope: {
      'model': '=pulldownModel'
    },
    templateUrl: LIB_ROOT + 'directives/pulldown.tpl.html',
    controller: function($scope) {
      $scope.model = {
        expanded: false,
        toggle: function() {
          this.expanded = !this.expanded;
        },
      }
    }
  }
});

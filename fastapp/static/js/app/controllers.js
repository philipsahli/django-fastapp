window.app = angular.module('execApp', ['ngGrid', 'base64', 'ngResource', 'baseServices']);

window.app.controller('BasesCtrl', ['$scope', 'Bases', 'Apy', function($scope, Bases, Apy) {
  $scope.init = function() {
    var bases = Bases.all(function() {
      angular.forEach(bases, function(base) {
        base.apy_models = Apy.all({'baseId': base.id});
      });
      $scope.bases = bases;
    });
  };
}]);


window.app.controller('ExecCtrl', ['$scope', '$http', '$base64', 'Apy', 'Apy1', function($scope, $http, $base64, Apy, Apy1) {
  $scope.new_exec_name = "";
  $scope.apys = [];

  $scope.init = function() {
    var apys= Apy.all({'baseId': window.active_base_id}, function() {
      $scope.apys = apys;
      counter=0;

      $scope.apys.map(function(apy) {
        console.log(counter);
        $scope.$watch(apy, function(changed) {
          console.log("changed");
        }, true);
        counter++;
      });
    });
  };

  $scope.create = function() {
    Apy.create({'baseId': window.active_base_id}, {'name': $scope.new_exec_name}, function(apy) {
      $scope.apys.push(apy);
      $scope.showNewExec = false;
    });
  };

  $scope.save= function(apy) {
    Apy1.update({'baseId': window.active_base_id, 'id': apy.id}, apy);
  };

  $scope.delete= function(apy) {
    //Apy1.update({'baseId': window.active_base_id, 'id': apy.id}, apy);
    console.log(apy);
    Apy1.delete({'baseId': window.active_base_id, 'id': apy.id}, function(data) {
      var indx = $scope.apys.indexOf(apy);
      $scope.apys.splice(indx, 1);
    });

  };

  $scope.clone= function(apy) {
    Apy1.clone({'baseId': window.active_base_id, 'id': apy.id}, apy, function(data) {
      $scope.apys.push(data);
    });
  };

  $scope.execute=function(apy) {
    Apy1.execute({'baseName': window.active_base, 'name': apy.name, 'json':""});
  };

  $scope.rename=function($event) {
    new_exec_name = $($event.currentTarget.parentNode.parentNode).find('input').first().val();
    this.apy.name = new_exec_name;
    $scope.save(this.apy);
  };

  /*$scope.$watch('apy.module', function(oldVal,newVal){
    console.log(oldVal);
    console.log(newVal);
    console.log("changed");
  });*/



}]);

var removeTemplate = '<button type="button" class="btn btn-default btn-xs" ng-click="delete()"><span class="glyphicon glyphicon-remove"></span> Delete</button>';
window.app.controller('SettingsCtrl', ['$scope', '$http', '$base64', 'Settings', 'Setting', function($scope, $http, $base64, Settings, Setting) {
  $scope.myData = [];
  $scope.gridOptions = {
    data: 'myData',
    selectedItems: [],
    enableSorting: true,
    sortInfo: {fields: ['key', 'value'], directions: ['asc']},
        //enableCellSelection: true,
        enableRowSelection: false,
        enableCellEditOnFocus: false,
        columnDefs: [{field: 'key', displayName: 'Key', enableCellEdit: true, width: 120},
        {field: 'value', displayName:'Value', enableCellEdit: true, editableCellTemplate: '<textarea row="1"  ng-class="\'colt\' + col.index" ng-input="COL_FIELD" ng-model="COL_FIELD" />'},
        {field: 'actions', displayName:'', enableCellEdit: false, cellTemplate: removeTemplate}
        ]
      };

      $scope.init = function() {
        $scope.myData = Settings.all({'baseId': window.active_base_id });
      };

      $scope.addRow = function() {
        $scope.myData.push({key: "key", value: "value"});
      };

      $scope.save = function() {
      // base64 output
      $scope.myData.map(function(item) {
        if (item.id===undefined) {
          new_item = Settings.create({'baseId': window.active_base_id}, item, function() {
            if (new_item['id']!==undefined) {
              item.id = new_item['id'];
            }
          });

        } else {
          Setting.update({'baseId': window.active_base_id, 'id': item.id}, item);
        }
      });
    };

    $scope.delete = function() {
      console.log(this.row);
      var index = this.row.rowIndex;
      $scope.gridOptions.selectItem(index, false);
      removed = $scope.myData.splice(index, 1);
      Setting.delete({'baseId': window.active_base_id, 'id': removed.id});
    };
}]);

window.app.directive('codemirror', function() {
  return {
    restrict: 'A',
    priority: 2,
    scope: {
      'apy': '=codemirror'
    },
    template: '{{apy.module}}',
    link: function(scope, elem, attrs) {
      //console.log(scope);
      //console.log(scope.apy);
      var myCodeMirror = CodeMirror(function(elt) {
        elem.parent().replaceWith(elt);
      }, {
        value: scope.apy.module,
        mode: {name: "text/x-cython",
        version: 2,
        singleLineStringErrors: false},
          //readOnly: "$window.readyOnly",
          lineNumbers: true,
          indentUnit: 4,
          tabMode: "shift",
          lineWrapping: true,
          indentWithTabs: true,
          matchBrackets: true,
          vimMode: true,
          showCursorWhenSelecting: true
        });
      myCodeMirror.on("blur", function(cm, cmChangeObject){
        console.log("scope.$apply");
        scope.$apply(function() {
          scope.apy.module = myCodeMirror.getValue();
        });
      });
    }
  };
});
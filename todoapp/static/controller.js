(function() {
  var app = angular.module("myApp", ["ui.router"]);
 app.constant('rootUrl', '{{ROOT_URL}}');
  app.run(function($rootScope, $location, $state, LoginService) {
    $rootScope.$on("$stateChangeStart", function(
      event,
      toState,
      toParams,
      fromState,
      fromParams
    ) {
      // console.log("Changed state to: " + toState);
    });
  });

// router
  app.config([
    "$stateProvider",
    "$urlRouterProvider",
    "$interpolateProvider",
    function($stateProvider, $urlRouterProvider,$interpolateProvider) {
      $interpolateProvider.startSymbol('{[{').endSymbol('}]}');
      $urlRouterProvider.otherwise("/login");

      $stateProvider
        .state("login", {
          url: "/login",
          templateUrl: "partials/login.html",
          controller: "LoginController"
        })
        .state("home", {
          url: "/home",
          templateUrl: "partials/home.html",
          controller: "HomeController"
        });
    }
  ]);

// loginctrl
  app.controller("LoginController", function(
    $scope,
    $rootScope,
    $stateParams,
    $state,
    LoginService
  ) {
    $rootScope.title = "User Login";
    $scope.alert = false;

    $scope.formSubmit = function() {
      LoginService.login($scope.username, $scope.password).success(function(data,status){
        
        LoginService.setLocalStorage("username", $scope.username);
        LoginService.setLocalStorage("password", $scope.password);
        LoginService.setLocalStorage("user", data.user);
        
          $state.transitionTo("home");
      })
      .error(function(data,status){
        
        
        if (status == 401){
          alert(data.error_message);
        }
        else{
          alert("Something went wrong");
        }

      });
    };
  });

// homectrl
  app.controller("HomeController", function(
    $scope,
    $rootScope,
    $stateParams,
    $state,
    HomeService,
    LoginService,$filter
  ) {
    $scope.add=false;
    $scope.addsub=false;
    $rootScope.title = "Todo";
    $scope.subdescription="";
    $scope.title="";
    $scope.description="";
    $scope.due_date="";
    $scope.taskid = 0;
    $scope.alert_hour=0;
    $scope.subtaskid=0;
    $scope.search_title='';
    $scope.loadTasks = function() {
      HomeService.load_tasks().success(function(data,status){
        $rootScope.task_data = data.objects;
        angular.forEach($rootScope.task_data,function(value, key) {
          value.due_date=$filter('date')(value.due_date, "dd/MM/yyyy");
        })
      })
      .error(function(data,status){
        if (status == 500){
          alert("Something went wrong"); 
        }
        else{
          alert(data.error_message);
        }
      });
    };


     $scope.searchTask = function() {
      HomeService.search__tasks($scope.search_title).success(function(data,status){
        $rootScope.task_data = data.objects;
      })
      .error(function(data,status){
        if (status == 500){
          alert("Something went wrong"); 
        }
        else{
          alert(data.error_message);
        }
      });
    };



    $scope.delete = function(task){
      
      HomeService.delete_tasks(task).success(function(data,status){
        $state.reload();
      })
      .error(function(data,status){
        if (status == 500){
          alert("Something went wrong"); 
        }
        else{
          alert(data.error_message);
        }
      });
    };

    $scope.deleteSub = function(subtask){
      
      HomeService.delete_tasks(subtask).success(function(data,status){
        
        $state.reload();
      })
      .error(function(data,status){
        
        if (status == 500){
          alert("Something went wrong"); 
        }
        else{
          alert(data.error_message);
        }
      });
    };

    $scope.addtodo = function(){
      $scope.add=true;
    };

    $scope.addSubtask = function(){
      $scope.addsub=true;
    };

    $scope.saveSubTask = function(task,subdescription){
      var data = {};
      data.description=subdescription;
      
      data.task=task.resource_uri;
      HomeService.add_subtasks(data).success(function(data,status){
        
        $state.reload();
      })
      .error(function(data,status){
        
        if (status == 500){
          alert("Something went wrong"); 
        }
        else{
          alert(data.error_message);
        }
      });
    };

    $scope.saveTask = function(){
      var data={};
      data.title=$scope.title;
      data.description= $scope.description;
      data.due_date=$scope.due_date;
      data.user = LoginService.getLocalStorage('user')
      HomeService.add_tasks(data).success(function(data,status){
        
        $state.reload();
      })
      .error(function(data,status){
        
        if (status == 500){
          alert("Something went wrong"); 
        }
        else{
          alert(data.error_message);
        }
      });
    };

    $scope.editTask = function(task){
      HomeService.edit_tasks(task).success(function(data,status){
        
        $state.reload();
        
      })
      .error(function(data,status){
        
        if (status == 500){
          alert("Something went wrong"); 
        }
        else{
          alert(data.error_message);
        }
      });
    };

    $scope.editSubTask = function(subtask){
      HomeService.edit_subtasks(subtask).success(function(data,status){
        
        $state.reload();
        
      })
      .error(function(data,status){
        
        if (status == 500){
          alert("Something went wrong"); 
        }
        else{
          alert(data.error_message);
        }
      });
    };

    $scope.loadTaskAlerts = function() {
      HomeService.load_task_alerts().success(function(data,status){
        $rootScope.task_alert_data = data.objects;
        
      })
      .error(function(data,status){
        
        if (status == 500){
          alert("Something went wrong"); 
        }
        else{
          alert(data.error_message);
        }
      });
    };

    $scope.loadTasks();
    $scope.loadTaskAlerts();
  });

  // });
// service
  app.factory("LoginService", function($http,rootUrl) {
    var admin = "admin";
    var pass = "pass";
    var isAuthenticated = false;

    return {

      encode: function (input) {
       var keyStr = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=';
           var output = "";
           var chr1, chr2, chr3 = "";
           var enc1, enc2, enc3, enc4 = "";
           var i = 0;

           do {
               chr1 = input.charCodeAt(i++);
               chr2 = input.charCodeAt(i++);
               chr3 = input.charCodeAt(i++);

               enc1 = chr1 >> 2;
               enc2 = ((chr1 & 3) << 4) | (chr2 >> 4);
               enc3 = ((chr2 & 15) << 2) | (chr3 >> 6);
               enc4 = chr3 & 63;

               if (isNaN(chr2)) {
                   enc3 = enc4 = 64;
               } else if (isNaN(chr3)) {
                   enc4 = 64;
               }

               output = output +
                   keyStr.charAt(enc1) +
                   keyStr.charAt(enc2) +
                   keyStr.charAt(enc3) +
                   keyStr.charAt(enc4);
               chr1 = chr2 = chr3 = "";
               enc1 = enc2 = enc3 = enc4 = "";
           } while (i < input.length);

           return output;
   },
   decode: function (input) {
        var keyStr = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=';
           var output = "";
           var chr1, chr2, chr3 = "";
           var enc1, enc2, enc3, enc4 = "";
           var i = 0;

           // remove all characters that are not A-Z, a-z, 0-9, +, /, or =
           var base64test = /[^A-Za-z0-9\+\/\=]/g;
           if (base64test.exec(input)) {
               window.alert("There were invalid base64 characters in the input text.\n" +
                   "Valid base64 characters are A-Z, a-z, 0-9, '+', '/',and '='\n" +
                   "Expect errors in decoding.");
           }
           input = input.replace(/[^A-Za-z0-9\+\/\=]/g, "");

           do {
               enc1 = keyStr.indexOf(input.charAt(i++));
               enc2 = keyStr.indexOf(input.charAt(i++));
               enc3 = keyStr.indexOf(input.charAt(i++));
               enc4 = keyStr.indexOf(input.charAt(i++));

               chr1 = (enc1 << 2) | (enc2 >> 4);
               chr2 = ((enc2 & 15) << 4) | (enc3 >> 2);
               chr3 = ((enc3 & 3) << 6) | enc4;

               output = output + String.fromCharCode(chr1);

               if (enc3 != 64) {
                   output = output + String.fromCharCode(chr2);
               }
               if (enc4 != 64) {
                   output = output + String.fromCharCode(chr3);
               }

               chr1 = chr2 = chr3 = "";
               enc1 = enc2 = enc3 = enc4 = "";

           } while (i < input.length);

           return output;
       },

      login: function(username, password) {
        var loginDetails={};
        loginDetails.username=username;
        loginDetails.password=password;
        
        return $http.post('/api/v1/user/login/', loginDetails);
      },

      getLocalStorage: function(key){
        var item = localStorage.getItem(key);
        data = JSON.parse(item);
        return data;
      },

      setLocalStorage: function(key, value){
        localStorage.setItem(key, JSON.stringify(value));
      },

      isAuthenticated: function() {
        return isAuthenticated;
      }
    };
  });


// homeservice
  app.factory("HomeService", function($http,rootUrl, LoginService, AuthService) {
    var admin = "admin";
    var pass = "pass";
    var isAuthenticated = false;

    return {
      load_tasks: function() {
        
        headers = {"Authorization": "Basic" + AuthService.create_auth()};
        
        return $http.get('/api/v1/task/get/', {headers: headers});
      },

      add_tasks: function(data) {
        headers = {"Authorization": "Basic" + AuthService.create_auth()};
        
        return $http.post('/api/v1/task/', data);
      },

      search__tasks: function(data) {
        
        headers = {"Authorization": "Basic" + AuthService.create_auth()};
        
        return $http.get('/api/v1/task/get/?title='+data);
      },

      add_subtasks: function(data) {
        headers = {"Authorization": "Basic" + AuthService.create_auth()};
        
        return $http.post('/api/v1/subtask/', data);
      },

      edit_tasks: function(data) {
        headers = {"Authorization": "Basic" + AuthService.create_auth()};
        
        return $http.put(data.resource_uri, data);
      },

      edit_subtasks: function(data) {
        headers = {"Authorization": "Basic" + AuthService.create_auth()};
        
        return $http.put(data.resource_uri, data);
      },

      delete_tasks: function(data) {
        headers = {"Authorization": "Basic" + AuthService.create_auth()};
        
        return $http.delete(data.resource_uri, data);
      },

      load_task_alerts: function() {
        
        headers = {"Authorization": "Basic" + AuthService.create_auth()};
        
        return $http.get('/api/v1/task/alert/get/', {headers: headers});
      },

      getLocalStorage: function(key){
        var item = localStorage.getItem(key);
        data = JSON.parse(item);
        return data;
      },

      setLocalStorage: function(key, value){
        localStorage.setItem(key, JSON.stringify(value));
      },

      isAuthenticated: function() {
        return isAuthenticated;
      }
    };
  });


// authservice
  app.factory("AuthService", function($http,rootUrl, LoginService) {
    var admin = "admin";
    var pass = "pass";
    var isAuthenticated = false;

    return {
      

       create_auth: function() {
        var username = LoginService.getLocalStorage("username");
        var password = LoginService.getLocalStorage("password");
        var auth = LoginService.encode(username+":"+password);
        return auth
      },
    };
  });

})();
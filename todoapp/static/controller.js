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
      console.log("Changed state to: " + toState);
    });

    // if (!LoginService.isAuthenticated()) {
    //   $state.transitionTo("login");
    // }
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
    $rootScope.title = "AngularJS Login Sample";

    $scope.formSubmit = function() {
      // if (LoginService.login($scope.username, $scope.password)) {
      //   $scope.error = "";
      //   $scope.username = "";
      //   $scope.password = "";
      //   $state.transitionTo("home");

      //   LoginService.login()
      // } else {
      //   $scope.error = "Incorrect username/password !";
      // }
      //  if () {
      //     $state.transitionTo("home");
      //  } else {
      //   $scope.error = "Incorrect username/password !";
      // }
      LoginService.login($scope.username, $scope.password).success(function(data,status){
        console.log(status)
        LoginService.setLocalStorage("username", $scope.username);
        LoginService.setLocalStorage("password", $scope.password);
        LoginService.setLocalStorage("user", data.user);
        console.log(LoginService.getLocalStorage("password"))
          $state.transitionTo("home");
      })
      .error(function(data,status){
        console.log(status)
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
    $rootScope.title = "AngularJS Login Sample";
    $scope.subdescription="";
    $scope.title="";
    $scope.description="";
    $scope.due_date="";
    $scope.taskid = 0;
    $scope.subtaskid=0;
    $scope.search_title='';
    $scope.loadTasks = function() {
      HomeService.load_tasks().success(function(data,status){
        console.log(status)
        // $scope.task_data = [];
        console.log(data)
        $rootScope.task_data = data.objects;
        angular.forEach($rootScope.task_data,function(value, key) {
          value.due_date=$filter('date')(value.due_date, "dd/MM/yyyy");
        })
        // $scope.formattedDate =   $filter('date')($scope.currDate, "dd-MM-yyyy");
        console.log(data.objects);
        // $scope.task_data.push.apply($scope.task_data,data.objects);
          // $state.transitionTo("home");
      })
      .error(function(data,status){
        console.log(status)
      });
    };


     $scope.searchTask = function() {
      console.log($scope.search_title)
      HomeService.search__tasks($scope.search_title).success(function(data,status){
        console.log(status)
        // $scope.task_data = [];
        console.log(data)
        $rootScope.task_data = data.objects;
        console.log(data.objects);
        // $scope.task_data.push.apply($scope.task_data,data.objects);
          // $state.transitionTo("home");
      })
      .error(function(data,status){
        console.log(status)
      });
    };



    $scope.delete = function(task){
      
      HomeService.delete_tasks(task).success(function(data,status){
        console.log(status)
        $state.reload();
        // $scope.task_data = [];
        // console.log(data)
        // $rootScope.task_data = data.objects;
        // console.log(data.objects);
        // $scope.task_data.push.apply($scope.task_data,data.objects);
          // $state.transitionTo("home");
      })
      .error(function(data,status){
        console.log(status)
      });
    }
    $scope.deleteSub = function(subtask){
      
      HomeService.delete_tasks(subtask).success(function(data,status){
        console.log(status)
        $state.reload();
        // $scope.task_data = [];
        // console.log(data)
        // $rootScope.task_data = data.objects;
        // console.log(data.objects);
        // $scope.task_data.push.apply($scope.task_data,data.objects);
          // $state.transitionTo("home");
      })
      .error(function(data,status){
        console.log(status)
      });
    }
    $scope.addtodo = function(){
      $scope.add=true;
    };
    $scope.addSubtask = function(){
      $scope.addsub=true;
    }
    $scope.saveaddsub = function(task,subdescription){
      var data = {};
      data.description=subdescription;
      console.log($scope.subdescription)
      data.task=task.resource_uri;
      HomeService.add_subtasks(data).success(function(data,status){
        console.log(status)
        $state.reload();
        // $scope.task_data = [];
        // console.log(data)
        // $rootScope.task_data = data.objects;
        // console.log(data.objects);
        // $scope.task_data.push.apply($scope.task_data,data.objects);
          // $state.transitionTo("home");
      })
      .error(function(data,status){
        console.log(status)
      });
    }
    $scope.savetodo = function(){
      var data={};
      data.title=$scope.title;
      data.description= $scope.description;
      data.due_date=$scope.due_date;
      data.user = LoginService.getLocalStorage('user')
      HomeService.add_tasks(data).success(function(data,status){
        console.log(status)
        $state.reload();
        // $scope.task_data = [];
        // console.log(data)
        // $rootScope.task_data = data.objects;
        // console.log(data.objects);
        // $scope.task_data.push.apply($scope.task_data,data.objects);
          // $state.transitionTo("home");
      })
      .error(function(data,status){
        console.log(status)
      });
    };
    $scope.saveeditedtodo = function(task){
      
      HomeService.edit_tasks(task).success(function(data,status){
        console.log(status)
        $state.reload();
        
      })
      .error(function(data,status){
        console.log(status)
      });
    };
    $scope.saveeditedsub = function(subtask){
      HomeService.edit_subtasks(subtask).success(function(data,status){
        console.log(status)
        $state.reload();
        
      })
      .error(function(data,status){
        console.log(status)
      });
    }

    $scope.loadTaskAlerts = function() {
      HomeService.load_task_alerts().success(function(data,status){
        console.log(status)
        console.log(data)
        $rootScope.task_alert_data = data.objects;
        // angular.forEach($rootScope.task_data,function(value, key) {
        //   value.due_date=$filter('date')(value.due_date, "dd/MM/yyyy");
        // })
        console.log(data.objects);
      })
      .error(function(data,status){
        console.log(status)
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
        // isAuthenticated = username === admin && password === pass;
        // return isAuthenticated;
        var loginDetails={};
        loginDetails.username=username;
        loginDetails.password=password;
        console.log(rootUrl);
        return $http.post('/api/v1/user/login/', loginDetails);
        // return $http.get(rootUrl + '/organic-product-order/', {headers: headers,
        //     params: {
        //         customer: customer,
        //         cycle:cycleId
        //     }
        // });
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
        // var loginDetails={};
        // loginDetails.username=username;
        // loginDetails.password=password;
        console.log(rootUrl);
        headers = {"Authorization": "Basic" + AuthService.create_auth()};
        console.log('headers', headers);
        return $http.get('/api/v1/task/get/', {headers: headers});
        // return $http.get(rootUrl + '/organic-product-order/', {headers: headers,
        //     params: {
        //         customer: customer,
        //         cycle:cycleId
        //     }
        // });
      },
      add_tasks: function(data) {
        // var loginDetails={};
        // loginDetails.username=username;
        // loginDetails.password=password;
        headers = {"Authorization": "Basic" + AuthService.create_auth()};
        console.log('headers', headers);
        return $http.post('/api/v1/task/', data);
        // return $http.get(rootUrl + '/organic-product-order/', {headers: headers,
        //     params: {
        //         customer: customer,
        //         cycle:cycleId
        //     }
        // });
      },

      search__tasks: function(data) {
        // var loginDetails={};
        console.log(data)
        // loginDetails.username=username;
        // loginDetails.password=password;
        headers = {"Authorization": "Basic" + AuthService.create_auth()};
        console.log('headers', headers);
        return $http.get('/api/v1/task/get/?title='+data);
        // return $http.get(rootUrl + '/organic-product-order/', {headers: headers,
        //     params: {
        //         customer: customer,
        //         cycle:cycleId
        //     }
        // });
      },

      add_subtasks: function(data) {
        // var loginDetails={};
        // loginDetails.username=username;
        // loginDetails.password=password;
        headers = {"Authorization": "Basic" + AuthService.create_auth()};
        console.log('headers', headers);
        return $http.post('/api/v1/subtask/', data);
        // return $http.get(rootUrl + '/organic-product-order/', {headers: headers,
        //     params: {
        //         customer: customer,
        //         cycle:cycleId
        //     }
        // });
      },
      edit_tasks: function(data) {
        // var loginDetails={};
        // loginDetails.username=username;
        // loginDetails.password=password;
        headers = {"Authorization": "Basic" + AuthService.create_auth()};
        console.log('headers', headers);
        return $http.put(data.resource_uri, data);
        // return $http.get(rootUrl + '/organic-product-order/', {headers: headers,
        //     params: {
        //         customer: customer,
        //         cycle:cycleId
        //     }
        // });
      },
      edit_subtasks: function(data) {
        // var loginDetails={};
        // loginDetails.username=username;
        // loginDetails.password=password;
        headers = {"Authorization": "Basic" + AuthService.create_auth()};
        console.log('headers', headers);
        return $http.put(data.resource_uri, data);
        // return $http.get(rootUrl + '/organic-product-order/', {headers: headers,
        //     params: {
        //         customer: customer,
        //         cycle:cycleId
        //     }
        // });
      },
      delete_tasks: function(data) {
        headers = {"Authorization": "Basic" + AuthService.create_auth()};
        console.log('headers', headers);
        return $http.delete(data.resource_uri, data);
      },

      load_task_alerts: function() {
        console.log(rootUrl);
        headers = {"Authorization": "Basic" + AuthService.create_auth()};
        console.log('headers', headers);
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
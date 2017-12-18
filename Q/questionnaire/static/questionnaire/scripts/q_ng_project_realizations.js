/* q_ng_project.js */
/* ng app for dealing w/ the main project page (not the management page) */

(function() {
    var app = angular.module("q_project", ["q_base"]);

    /**********/
    /* CONFIG */
    /**********/

    app.config(['$httpProvider', '$provide', function($httpProvider, $provide) {
        /* NG serializes data as pure JSON, while Django expects form parameters */
        /* TODO: SIMPLIFY THIS AS PER: https://stackoverflow.com/a/20276775/1060339 */
        /* TODO: MOVE THIS AJAX LOGIC INTO q_base */
        $httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8';
        $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    }]);

    /*******/
    /* RUN */
    /*******/

//    app.run(["$rootScope", function($rootScope) {
//        /* in theory, factories are preferred for global functionality */
//        /* b/c they isolate scope, but this is still sometimes useful */
//    }]);

    /*************/
    /* FACTORIES */
    /*************/

    /**************/
    /* DIRECTIVES */
    /**************/

    /***************/
    /* CONTROLLERS */
    /***************/

    /* don't generally need $scope for ng > 1.3 */
    /* except for the built-in scope fns (like $watch, $apply, etc.) */
    /* so I include it and use it in rare occasions */
    /* see http://toddmotto.com/digging-into-angulars-controller-as-syntax/ */

    app.controller("ProjectController", [ "$http", "$q", "$global_services", "$parse", "$scope", function($http, $q, $global_services, $parse, $scope) {

        var project_controller = this;

        project_controller.read_only = read_only;

        project_controller.is_loaded = false;
        project_controller.project = {}

        var project_api_url = "/api/qprojectlite/" + project_id;
        var document_api_url = "/api/qrealizationlite/?project=" + project_id;

        project_controller.blocking = function() {
            return $global_services.getBlocking();
        };

        project_controller.load = function() {
            var deferred = $q.defer();
            var asynch_calls = [
                $http.get(project_api_url),
                $http.get(document_api_url)
            ];
            $global_services.setBlocking(true);
            $q.all(asynch_calls).then(
                function(responses) {
                    project_controller.project = responses[0].data;
                    project_controller.documents = responses[1].data;
                    deferred.resolve(responses)
                    project_controller.is_loaded = true;
                    $global_services.setBlocking(false);
                },
                function(responses) {
                    deferred.reject(responses)
                    show_msg("Error retrieving project information.", "error");
                    project_controller.is_loaded = false;
                    $global_services.setBlocking(false);
                }
            )
            return deferred.promise;
        }

        project_controller.load()

        project_controller.project_join_request = function(user_id) {
            alert("todo")
        }

        project_controller.print_stuff = function() {
            console.log(project_controller.project);
        };
    }]);

    /***********/
    /* THE END */
    /***********/

})();
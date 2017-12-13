/* q_ng_index.js */
/* ng app for dealing w/ the index page */

(function() {
    var app = angular.module("q_index", ["q_base"]);

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

    app.controller("IndexController", [ "$http", "$global_services", "$parse", "$scope", function($http, $global_services, $parse, $scope) {

        var index_controller = this;

        index_controller.read_only = read_only;

        index_controller.is_loaded = false;
        index_controller.projects = [];

        var api_url = "/api/qprojectlite/";

        index_controller.blocking = function() {
            return $global_services.getBlocking();
        };

        index_controller.load = function() {
            $global_services.setBlocking(true);
            $http({
                method: "GET",
                url: api_url,
            }).then(
                /* success block */
                function(response) {
                    index_controller.projects = response.data.results;
                    index_controller.is_loaded = true;
                },
                /* error block */
                function(response) {
                    console.log(response.data);
                    show_msg("Error retrieving projects.", "error");
                }
            ).finally(function() {
                $global_services.setBlocking(false);
            });
        }

        index_controller.load()

    }]);

    /***********/
    /* THE END */
    /***********/

})();
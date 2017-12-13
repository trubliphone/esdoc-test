/* q_ng_users.js */
/* ng app for dealing w/ QUserProfile */

(function() {
    var app = angular.module("q_user", ["q_base"]);

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

    app.controller("UserController", [ "$http", "$q", "$global_services", "$parse", "$scope", function($http, $q, $global_services, $parse, $scope) {

        var user_controller = this;

        user_controller.is_valid = false;
        user_controller.is_pending = false;
        user_controller.read_only = read_only;

        user_controller.is_loaded = false;
        user_controller.proxy = {};
        user_controller.customization = {};
        user_controller.realization = {};

        var static_url = "/services/static/quserprofile/";
        var api_url = "/api/quserprofile/" + user_profile_id + "/";

        user_controller.blocking = function() {
            return $global_services.getBlocking();
        };

        /* I just use $q explicitly in the "load" fn to chain together asynchronous requests */
        /* $http uses $q implicitly, so the "submit" fn is fine as-is */

        user_controller.load = function() {
            var deferred = $q.defer();
            var asynch_calls = [
                $http.get(api_url),
                $http.get(static_url)
            ];
            $global_services.setBlocking(true);
            $q.all(asynch_calls).then(
                function(responses) {
                    // this is  a little bit contrived b/c the proxy & customization are both set to the same "static" serialization
                    user_controller.realization = responses[0].data;
                    user_controller.proxy = responses[1].data;
                    user_controller.customization = responses[1].data;
                    deferred.resolve(responses)
                    user_controller.is_loaded = true;
                    $global_services.setBlocking(false);
                },
                function(responses) {
                    deferred.reject(responses)
                    user_controller.is_loaded = false;
                    $global_services.setBlocking(false);
                }
            )
            return deferred.promise;
        }

        user_controller.submit = function() {
            $global_services.setBlocking(true);
            $http({
                method: "PUT",
                url: api_url,
                data: user_controller.realization
            }).then(
                /* success block */
                function(response) {
                    show_msg("Successfully updated user.", "success");
                },
                /* error block */
                function(response) {
                    console.log(response.data);
                    show_msg("Error updating user.", "error");
                }
            ).finally(function() {
                $global_services.setBlocking(false);
            });
        }

        user_controller.load()

//        /* TODO: SHOULD THIS USE $global_services.is_loaded INSTEAD ? */
//        $scope.$watch(function() {return user_controller.is_loaded;},
//            function (is_loaded) {
//                if (is_loaded) {
//                    user_controller.is_loaded = true;
//
//                    /* now that the model is loaded, we can do stuff... */
//
//                    user_controller.fields = [
//                        {
//                            model: "profile.user.first_name",
//                            name: "first_name",
//                            title: "First Name",
//                            type: "string",
//                            placeholder: "what's your first name?",
//                            help_text: "",
//                            inline_help: false,
//                            is_required: false,
//                            is_editable: true,
//                            is_displayed: true,
//                            order: 0,
//                            validators: [
//                                {
//                                    "name": "notfoo",
//                                    "fn_name": "validate_not_foo",
//                                    "msg": "<span class='glyphicon glyphicon-remove'/> you can't be foo!<br/>(I am a <em>synchronous</em> validator)",
//                                    "asynchronous": false
//                                },
//                                {
//                                    "name": "notbar",
//                                    "fn_name": "validate_not_bar",
//                                    "msg": "<span class='glyphicon glyphicon-remove'/>you can't be bar!<br/>(I am an <em>asynchronous</em> validator)",
//                                    "asynchronous": true
//                                }
//                            ]
//                        },
//                        {
//                            model: "profile.user.last_name",
//                            name: "last_name",
//                            title: "Last Name",
//                            type: "string",
//                            placeholder: "what's your last name?",
//                            help_text: "",
//                            inline_help: false,
//                            is_required: false,
//                            is_editable: true,
//                            is_displayed: true,
//                            order: 1,
//                            validators: [
//                            ]
//                        },
//                        {
//                            model: "profile.user.email",
//                            name: "email",
//                            title: "Email",
//                            type: "email",
//                            placeholder: "",
//                            help_text: "",
//                            inline_help: false,
//                            is_required: true,
//                            is_editable: false,
//                            is_displayed: true,
//                            order: 2,
//                            validators: [
//                            ]
//                        },
//                        {
//                            model: "profile.description",
//                            name: "description",
//                            title: "Description",
//                            type: "text",
//                            placeholder: "Tell us about yourself!",
//                            help_text: "asdf",
//                            inline_help: false,
//                            is_required: false,
//                            is_editable: true,
//                            is_displayed: true,
//                            order: 2,
//                            validators: [
//                                {
//                                /* NOTICE MY LIL' HACK */
//                                /* NG AUTOMATICALLY VALIDATES "[type='number']" INPUTS ACCORDING TO IT'S OWN RULES */
//                                /* FAIR ENOUGH, BUT WHEN A FIELD DOESN'T VALIDATE ACCORDING TO NG BUT DOES VALIDATE ACCORDING TO MY OWN VALIDATORS */
//                                /* THEN I GET AN ERROR W/ NO ASSOCIATED MESSAGE */
//                                /* TO GET AROUND THIS, I SET "name" BELOW TO BE THE SAME NAME USED INTERNALLY BY NG */
//                                /* HOORAY! */
//                                    "name": "number",
//                                    "fn_name": "validate_int",
//                                    "msg": "<span class='glyphicon glyphicon-remove'/> this must be an integer",
//                                    "asynchronous": false
//                                }
//                            ]
//                        },
//                        {
//                            model: "profile.institute",
//                            name: "institute",
//                            title: "Institute",
//                            type: "enumeration",
//                            enumeration_choices: [
//                                {
//                                    "value": "One",
//                                    "order": 0,
//                                    "documentation": "here is <em>some</em> help"
//                                },
//                                {
//                                    "value": "Two",
//                                    "order": 1,
//                                    "documentation": ""
//                                }
//                            ],
//                            enumeration_open: false,
//                            enumeration_multiple: false,
//                            placeholder: "",
//                            help_text: "Please select the institute for which you intend to publish documents. If no selection is made, you will be unable to publish.",
//                            inline_help: false,
//                            is_required: false,
//                            is_editable: true,
//                            is_displayed: true,
//                            order: 3,
//                            validators: [
//                            ]
//                        }
//                    ]
//                }
//            }
//        );

        user_controller.resend_verification = function() {
            var resend_verification_url = "/services/accounts/send_email_confirmation/";
            var resend_verification_data = $.param({
                username: user_controller.profile.user.username
            });
            $global_services.setBlocking(true);
            $http({
                method: "POST",
                url: resend_verification_url,
                data: resend_verification_data,
            }).then(
                /* success block */
                function(response) {
                    check_msg();
                },
                /* error block */
                function(response) {
                    console.log(response);
                    check_msg();
                }
            ).finally(function() {
                $global_services.setBlocking(false);
            });
        };

        /* TODO: SOMEHOW MOVE THIS TO ROOT SCOPE */

        $scope.propertify = function (string) {
            /* takes a string and evaluates it against the current scope */
            /* used for dynamic 'ng-model' attributes */
            /* (taken from https://stackoverflow.com/a/42562330/1060339) */
            var property = $parse(string);
            return function (new_val) {
                if (arguments.length) {
                    /* assign new_val to property */
                    newVal = angular.isDefined(new_val) ?  new_val : "";
                    property.assign($scope, new_val);
                }
                /* assign property to new_val */
                return property($scope);
            };
        };

        $scope.get_object_by_attr = function(objs, attr) {
            return get_object_by_attrs(objs, attr);
        };

        user_controller.print_stuff = function() {
            console.log(user_controller.realization);
            console.log(user_controller.customization);
            console.log(user_controller.proxy);
        };

    }]);

    /***********/
    /* THE END */
    /***********/

})();
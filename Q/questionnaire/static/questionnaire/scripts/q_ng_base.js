/* q_base.js */

/* angular app for Questionnaire */
/* all page-specific apps inherit from this */

(function() {
    var app = angular.module("q_base", ["ngSanitize", "ui.bootstrap"]);

    /**********/
    /* CONFIG */
    /**********/

    /*******/
    /* RUN */
    /*******/

    app.run(["$rootScope", function($rootScope) {

        /* in general, services/factories are preferred to run for sharing functionality */
        /* b/c run doesn't isolate scope, so only put codehere that doesn't modify scope */

    }]);

    /***************/
    /* CONTROLLERS */
    /***************/

    /*************/
    /* FACTORIES */
    /*************/

    app.factory('$global_services', ['$http', '$q', function($http, $q) {

        var _blocking = false;

        var _is_loaded = false;

	    var _DATA =  {};  /* (top-level controller resets this) */

        var proxy = {};
        var customization = {};
        var realization = {};

	    return {
            /* (re)load data */

            load: function(data, flag) {
                var deferred = $q.defer();
                _blocking = true;
                $http(data).then(
                    /* success block */
                    function(response) {
//                        return deferred.resolve();
console.log(response)
                        deferred.resolve();
                        return response.data;
                    },
                    /* error block */
                    function(response) {
                        console.log(response);
//                        return deferred.reject();
                        deferred.reject();
                        return null;
                    }
                ).finally(
                    _blocking = false
                )
                return deferred.promise;
            },



//
//
//                _blocking = true;
//                $http(data).then(
//                    /* success block */
//                    function(response) {
//                        model = response.data;
//                        console.log(model)
//                        flag = true;
//                    },
//                    /* error block */
//                    function(response) {
//                        console.log(response);
//                        flag = false;
//                    }
//                ).finally(
//                    _blocking = false
//                )
//            },
//
//            load: function(url) {
//                /* TODO: UPDATE THIS FN W/ NEW "$q" SERVICE */
//                var promise = $http.get(url, {format: "json"})
//                    .success(function (data) {
//                        _DATA = data;
//                        _is_loaded = true;
//                    })
//                    .error(function (data) {
//                        console.log(data);
//                        _is_loaded = false;
//                    });
//                return promise;
//            },
            /* work out if data has been loaded */
            isLoaded: function() {
                return _is_loaded;
            },
            /* work out if interaction should be blocked */
            getBlocking: function() {
                return _blocking;
            },
            /* toggle interaction */
            setBlocking: function(blocking) {
                _blocking = blocking;
            },
            /* get the entire model all at once */
            getData: function() {
                return _DATA;
            }
        };

    }]);

    app.factory('$qvalidators', ['$http', function($http) {

        var DEFAULT_MAX_LENGTH = 30;

        /* for consistency's sake, where appropriate, use the same regex as the built-in ng ones [https://github.com/angular/angular.js/blob/master/src/ng/directive/input.js] */
        var NG_URL_REGEXP = /^[a-z][a-z\d.+-]*:\/*(?:[^:@]+(?::[^@]+)?@)?(?:[^\s:/?#]+|\[[a-f\d:]+])(?::\d+)?(?:\/[^?#]*)?(?:\?[^#]*)?(?:#.*)?$/i;
        var NG_EMAIL_REGEXP = /^(?=.{1,254}$)(?=.{1,64}@)[-!#$%&'*+/0-9=?A-Z^_`a-z{|}~]+(\.[-!#$%&'*+/0-9=?A-Z^_`a-z{|}~]+)*@[A-Za-z0-9]([A-Za-z0-9-]{0,61}[A-Za-z0-9])?(\.[A-Za-z0-9]([A-Za-z0-9-]{0,61}[A-Za-z0-9])?)*$/;
        var NG_NUMBER_REGEXP = /^\s*(-|\+)?(\d+|(\d*(\.\d*)))([eE][+-]?\d+)?\s*$/;
        var NG_DATE_REGEXP = /^(\d{4,})-(\d{2})-(\d{2})$/;
        var NG_TIME_REGEXP = /^(\d\d):(\d\d)(?::(\d\d)(\.\d{1,3})?)?$/;

        /* be wary of using too many asynchronous validators... they can make things slow */

        function asynchronous_validator(data, promise) {
            var asynchronous_validator_url = "/services/validate/";
            $http({
                method: "POST",
                url: asynchronous_validator_url,
                data: data
            }).then(
                /* success block */
                function(response) {
                    if (response.data == true) {
                        return promise.resolve()
                    }
                    else {
                        return promise.reject()
                    }
                },
                /* error block */
                function(response){
                    /* TODO: SHOULD I REALLY LET ERRORS PASS ? */
                    console.log(response)
                    return promise.resolve();
                }
            );
        }

	    return {

            /*****************************************/
            /* define all form/field validators here */
            /*****************************************/


            max_length_validator: function(old_value, new_value, max_length) {
               if(typeof options === "undefined") {
                    max_length = DEFAULT_MAX_LENGTH;
                }

                return new_value.length < max_length;
            },

            int_validator: function(old_value, new_value) {
                /* rather than rely on regex, I convert it to a number first */
                /* (this is to cope more leniently w/ scientific notation) */
                var converted_value = Number(new_value);
                var validated_value = converted_value ? Number.isInteger(converted_value) : false
                return validated_value;
            },

            float_validator: function(old_value, new_value) {
                /* rather than use a regex, I convert it to a number first */
                /* (this is to cope more leniently w/ scientific notation) */
                var converted_value = Number(new_value);
                return converted_value || false;
            },

            email_validator: function(old_value, new_value) {
                return NG_EMAIL_REGEXP.test(new_value);
            },

            not_foo_validator: function(old_value, new_value) {
                return new_value.toLowerCase() != "foo";
            },

            not_bar_validator: function(old_value, new_value, promise) {
                var validator_data = $.param({
                    validator: "validate_not_bar",
                    old_value: old_value,
                    new_value: new_value
                });
                return asynchronous_validator(validator_data, promise);
            }

        };

    }]);

    /**************/
    /* DIRECTIVES */
    /**************/

    /**********************************************/
    /* run some fn _after_ a DOM element is ready */
    /**********************************************/

    /* thanks to: https://stackoverflow.com/a/29571230/1060339 */

    app.directive("elementReady", ['$parse', '$global_services', function($parse, $global_services) {
        return {
            restrict: "A",
            link: function(scope, element, attrs) {
                element.ready(function() {
//                    $global_services.setBlocking(true);
                    scope.$apply(function() {
                        var fn = $parse(attrs.elementReady);
                        fn(scope);
                    });
//                    $global_services.setBlocking(false);
                });
            }
        }
    }]);

    /*************************************************/
    /* track the status of dynamically-created forms */
    /*************************************************/

    app.directive('watchFormValidity', ['$parse', function($parse) {
        return {
            restrict: "A",
            scope: false,
            link: function (scope, element, attrs) {
                var scope_variable = $parse(attrs["watchFormValidity"])
                var form_name = attrs["name"];

                var form_validity_expression = form_name + ".$valid";
                var form_pending_expression = form_name + ".$pending";

                scope.$watchGroup([form_validity_expression, form_pending_expression], function(form_status) {
                    var form_validity = form_status[0];
                    /* ("$pending" is undefined for forms w/out asynchronous validation enabled) */
                    var form_pending = typeof form_status[1] !== "undefined" ? form_status[1] : false;
                    scope_variable.assign(scope, form_validity && !form_pending);
                });
//                scope.$watch(form_validity_expression, function (form_validity) {
//                    scope_variable.assign(scope, form_validity);
//                });
            }
        }
    }]);

    /**************************/
    /* dynamic error handling */
    /**************************/

    app.directive('qvalidators', ['$compile', '$qvalidators', '$q', function($compile, $qvalidators, $q) {
        return {
            require: ['^form', 'ngModel'],
            scope: {
                validators: "=qvalidators"
            },
            transclude: true,
            link: function(scope, elm, attrs, ctrls) {
                var form = ctrls[0];
                var ctrl = ctrls[1];
                var error_elm = elm.parent().find(".error[for='" + elm.attr("id") + "']");
                if (!error_elm.exists()) {
                    console.log("WARNING: unable to find an error section for " + elm.attr("id"));
                }
                $.each(scope.validators, function(i, validator) {
                    var validator_fn = $qvalidators[validator.fn_name]
                    if (validator.asynchronous) {
                        ctrl.$asyncValidators[validator.name] = function(modelValue, viewValue) {
                            var deferred = $q.defer();
                            validator_fn(modelValue, viewValue, deferred)
                            return deferred.promise;
                        }
                    }
                    else {
                        ctrl.$validators[validator.name] = function(modelValue, viewValue) {
                            if (ctrl.$isEmpty(modelValue)) {
                                return true;
                            }
                            return validator_fn(modelValue, viewValue);
                        };
                    }
                    var error_class = [form.$name, ctrl.$name, "$error", validator.name].join(".");
                    var error_content = "<div class='error_msg' ng-show='" + error_class + "'>" + validator.msg + "</div>"
                    var compiled_error_content = $compile(error_content)(scope.$parent)
                    error_elm.append(compiled_error_content);
                });
            }
        };
    }]);

    /*********************************/
    /* add attrs from customizations */
    /*********************************/

    app.directive('customAttrs', function() {
        return {
            restrict: "A",
//            scope: {
//                customAttrs: '='
//            },
            link: function($scope, $element, $attrs) {
                $scope.custom_attrs = angular.fromJson($attrs['customAttrs']);
                angular.forEach($scope.custom_attrs, function(attr_value, attr_key) {
                    var existing_attr_value = $element.attr(attr_key);
                    if (typeof existing_attr_value !== typeof undefined && existing_attr_value !== false) {
                        /* attr_key already exists */
                        $element.attr(attr_key, existing_attr_value + " " + attr_value)
                    }
                    else {
                        /* attr_key does not exist */
                        $element.attr(attr_key, attr_value);
                    }
                });
            }
        }
    });

    /********************/
    /* make help pretty */
    /********************/

    app.directive('popover', ['$compile', function($compile) {
        return {
            scope: {
                popoverText: "@"
            },
            link: function(scope, elm, attrs, ctrl) {
                $(elm).attr({
                    "data-toggle": "popover",
                    "tabindex": "0",
                    "role": "button"
                }).popover({
                    "placement": "top",
                    "content": scope.popoverText,
                    "html": true,
                    "trigger": "focus",
                });
            }
        }
    }]);

    /***********************/
    /* make selects pretty */
    /***********************/

    app.directive('enumeration', ['$compile', '$templateRequest', function($compile, $templateRequest) {
        return {
            require: ['^form', 'ngModel'],
            scope: {
                enumerationChoices: "=",
                enumerationOpen: "=",
                enumerationMultiple: "=",
            },
            replace: false,
            templateUrl: "/static/questionnaire/templates/q_ng_enumeration.html",
            link: function ($scope, $element, $attrs, $ctrls) {

                var form_controller = $ctrls[0];
                var model_controller = $ctrls[1];

                $scope.TITLE_LIMIT = 2;
                $scope.is_loaded = false;
                $scope.is_open =  $scope.enumerationOpen;
                $scope.is_multiple = $scope.enumerationMultiple;
                if ($scope.is_open) {
                    $scope.title_placeholder = "<span class='placeholder'>Please select option(s)</span>";
                }
                else {
                    $scope.title_placeholder = "<span class='placeholder'>Please select an option</span>";
                }

                $templateRequest("/static/questionnaire/templates/q_ng_enumeration.html").then(function(response){
                    /* this little bit of code is required to compile any ng stuff in the template */
                    var template = angular.element(response);
                    $compile(template)($scope);
                    $element.after(template);
                });

                $scope.$watch(function () {
                    return model_controller.$modelValue;
                }, function(model_value) {
                    /* initialize the enumeration as soon as the modelValue changes for the 1st time */
                    if (! $scope.is_loaded) {
                        $.each($scope.enumerationChoices, function(i, choice) {
                            if (model_value.indexOf(choice.value) !== -1) {
                                choice.is_active = true;
                                $scope.select_choice(choice);
                            }
                        })
                        $scope.is_loaded = true
                    }
                });

                $scope.get_enumeration_title = function () {
                    var active_choices = $scope.get_active_choices();
                    var active_choices_length = active_choices.length;
                    if (active_choices_length == 0) {
                        /* no choices are made, show the default title... */
                        return $scope.title_placeholder;
                    }
                    else if (active_choices_length <= $scope.TITLE_LIMIT ) {
                        /* some choices are made, show them... */
                        var formatted_choices = $.map(active_choices, function(choice) {
                            return "\"" + choice.title + "\"";
                        })
                        return formatted_choices.join(", ");
                    }
                    else {
                        /* loads of choices are made, show TITLE_LIMIT of them... */
                        var formatted_choices = $.map(active_choices.slice(0, $scope.TITLE_LIMIT), function(choice) {
                            return "\"" + choice.title + "\"";
                        })
                        return formatted_choices.join(", ") + "<em>...plus " + (active_choices_length - $scope.TITLE_LIMIT) + " more</em>";
                    }
                }

                $scope.get_active_choices = function() {
                    var active_choices = $.grep($scope.enumerationChoices, function(choice, index) {
                        return choice.is_active == true;
                    })
                    return active_choices;
                }

                $scope.select_choice = function(choice) {
                    var current_choices = model_controller.$modelValue;
                    if ($scope.is_multiple) {
                    }
                    else {
                        if (choice.is_active) {
                            $.each($scope.enumerationChoices, function (index, c) {
                                if (c != choice) {
                                    c.is_active = false;
                                }
                            });
                            current_choices.splice(0, current_choices.length);
                            current_choices.push(choice.value);
                        }
                        else {
                            current_choices.splice(0, current_choices.length);
                        }
                    }
                    /* strictly speaking, I don't have to re-render the underlying control, but it makes me happy to do so */
                    model_controller.$setViewValue(current_choices);
                    model_controller.$render();
                }
            }
        }
    }]);

    /***********/
    /* THE END */
    /***********/

})();
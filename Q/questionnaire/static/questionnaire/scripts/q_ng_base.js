/* q_base.js */

/* angular app for Questionnaire */
/* all page-specific apps inherit from this */

(function() {
    var app = angular.module("q_base", ["ngSanitize"]);

    /**********/
    /* CONFIG */
    /**********/

    /*******/
    /* RUN */
    /*******/

    app.run(["$rootScope", function($rootScope) {

        /* in general, services/factories are preferred to run for sharing functionality */
        /* b/c run doesn't isolate scope, but this code doesn't modify scope, so I don't care */

        /* TODO: SHOULD I DEFINE THIS IN PYTHON AND LOAD IT AS NEEDED ? */
        var _FIELD_TYPES = {
            "string" : {
                "tag": "input",
                "title": "character string",
                "type": "text",
                "attrs": []
            },
            "text" : {
                "tag": "textarea",
                "title": "text",
                "type": null,
                "attrs": []
            },
            "bool": {
                "tag": "input",
                "title": "boolean value",
                "type": "radio",
                "attrs": []
            },
            "int" : {
                "tag": "input",
                "title": "integer",
                "type": "number",
                "attrs": []
            },
            "float" : {
                "tag": "input",
                "title": "floating-point number",
                "type": "number",
                "attrs": []
            },
            "url" : {
                "tag": "input",
                "title": "URL",
                "type": "url",
                "attrs": []
            },
            "email": {
                "tag": "input",
                "title": "email address",
                "type": "text",
                "attrs": []
            },
            "date": {
                "tag": "input",
                "title": "date",
                "type": "text",
                "attrs": []
            },
            "datetime" : {
                "tag": "input",
                "title": "date and time",
                "type": "text",
                "attrs": []
            },
            "time": {
                "tag": "input",
                "title": "time",
                "type": "text",
                "attrs": []
            },
            "enumeration": {
                "tag": "select",
                "title": "enumeration",
                "type": "text",
                "attrs": []
            },
            "relation": {
                "tag": "input",
                "title": "relation to other object",
                "type": "text",
                "attrs": []
            },
            "reference": {
                "tag": "input",
                "title": "reference to other document",
                "type": "text",
                "attrs": []
            }
        }
        var _DEFAULT_FIELD_TYPE_KEY = "string"  /* the field_type to use when all else fails */
        $rootScope.get_field_type = function(type_key) {
            if (_FIELD_TYPES.hasOwnProperty(type_key)) {
                return _FIELD_TYPES[type_key];
            }
            else {
                console.log("WARNING: unable to find field_type '" + type_key + "'.");
                return FIELD_TYPES[_DEFAULT_FIELD_TYPE_KEY];
            }
        } ;

    }]);

    /***************/
    /* CONTROLLERS */
    /***************/

    /*************/
    /* FACTORIES */
    /*************/

    app.factory('$global_services', ['$http', function($http) {

        var _blocking = false;

        var _is_loaded = false;

	    var _DATA =  {};  /* (top-level controller resets this) */

	    return {
            /* (re)load data */
            load: function(url) {
                /* TODO: UPDATE THIS FN W/ NEW "$q" SERVICE */
                var promise = $http.get(url, {format: "json"})
                    .success(function (data) {
                        _DATA = data;
                        _is_loaded = true;
                    })
                    .error(function (data) {
                        console.log(data);
                        _is_loaded = false;
                    });
                return promise;
            },
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

            validate_not_foo: function(old_value, new_value) {
                return new_value.toLowerCase() != "foo";
            },

            validate_not_bar: function(old_value, new_value, promise) {
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

    /***********/
    /* THE END */
    /***********/

})();
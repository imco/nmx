'use strict';

/**
 * @ngdoc function
 * @name frontendApp.controller:NormasmexicanasCtrl
 * @description
 * # NormasmexicanasCtrl
 * Controller of the frontendApp
 */
angular.module('frontendApp')
    .controller('NormasmexicanasCtrl', function($scope, $location, datos, $routeParams, socialShareImco) {
        $scope.listadoNMXsActual = [];
        $scope.buscar = {};
        $scope.resultados = 150;

        datos.getCTNN().then(function(result) {
            $scope.ctnns = result;
        })

        if ($routeParams.clave) {
            $scope.claveActual = decodeURIComponent($routeParams.clave);
            datos.getNMX($scope.claveActual).then(function(datos1) {
                $scope.normaActual = datos1;
                console.log('NOM:  ', datos1);

            });
        } else if ($routeParams.keyword) {
            $scope.keyword = decodeURIComponent($routeParams.keyword);
            datos.getFullKeyWord($scope.keyword).then(function(datos) {
                $scope.listadoNMXsActual = datos;
                $scope.resultados = datos.length;
                $scope.slider = {
                    value: datos.length,
                    options: {
                        floor: 0,
                        ceil: datos.length
                    },
                    onEnd: function() {
                        $scope.resultados = $scope.slider.value;
                    }
                };


            });
        } else {
            datos.getListadoNMX().then(function(result) {
                console.warn(result);
                $scope.listadoNMXsActual = result;
                $scope.slider = {
                    value: 150,
                    options: {
                        floor: 0,
                        ceil: result.length
                    },
                    onEnd: function() {
                        $scope.resultados = $scope.slider.value;
                    }
                };
            });
        }



        $scope.accederNorma = function accederNorma(claveNOM) {
            //console.log('accederNorma' + claveNOM);
            $location.path('/nmx/' + encodeURIComponent(claveNOM));
        };
        $scope.irONN = function(clave) {
            //console.log('accederNorma' + claveNOM);
            $location.path('/onn/' + encodeURIComponent(clave));
        };
        $scope.irCTNN = function(clave) {
            //console.log('accederNorma' + claveNOM);
            $location.path('/ctnn/' + encodeURIComponent(clave));
        };

        var facebookM = {
            capiton: 'Todo sobre la norma',


        };

        var tweetM = {};
        $scope.tweet = function() {
            tweetM.text = 'Todo sobre la norma: ' + $scope.claveActual + ', en';
            socialShareImco.tweet(tweetM);
        };
        $scope.facebook = function() {
            facebookM.capiton = 'Todo sobre la norma: ' + $scope.claveActual + ', en';
            facebookM.link = $location.absUrl();
            facebookM.redirect_uri = $location.absUrl();
            socialShareImco.facebook(facebookM);
        };


    });

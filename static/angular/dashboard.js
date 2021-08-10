var dashboardApp = angular.module('dashboardModule', []);

dashboardApp.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

dashboardApp.controller(
	'dashboardController',
	function($scope, $http) {
		$scope.newEvent = {
			name: null,
			start_time: "01:00 PM",
			end_time: "02:15 PM"
		}

		$scope.addEvent = function() {
			$http.put(
				'/calendar/api/dashboard/event/',
				{
					'name': $scope.newEvent.name,
					'start_time': $scope.newEvent.start_time,
					'end_time': $scope.newEvent.end_time,
				}
			).then(function(response){
				$scope.events = response.data.events;
				$scope.newEvent.name = '';
			});
		}

		$scope.deleteEvent = function(event) {
			$http.delete(
				'/calendar/api/dashboard/event/' + event.pk + '/'
			).then(function(response){
				$scope.events.splice($scope.events.indexOf(event), 1);
			});
		}

		$scope.addTask = function(goal, newTask) {
			$http.put(
				'/calendar/api/dashboard/goal/' + goal.pk + '/tasks/',
				{
					'name': newTask
				}
			).then(
				function(response) {
					goal.dropzones.todo.tasks.push(response.data.task);
					document.getElementById('id_newTask_' + goal.pk).value = '';
				}
			)
		}

		$scope.addGoal = function(objKey, goalObj) {
			$http.put(
				'/calendar/api/dashboard/goal/',
				{
					'target': objKey, 
					'name': goalObj
				}
			).then(
				function(response) {
					if(objKey == 'day') {
						$scope.dropzones.todo.goals.push(response.data.goal);
					}
					$scope.goalObj = '';
				}
			)
		}

		$scope.advanceGoal = function(goal, dropzone) {
			$http.patch(
				'/calendar/api/dashboard/goal/',
				{
					'pk': goal.pk,
					'status': dropzone.nextCol,
				}
			).then(
				function(response) {
					dropzone.goals.splice(dropzone.goals.indexOf(goal), 1);
					$scope.dropzones[dropzone.nextCol].goals.unshift(goal);
				}
			)
		}

		$scope.archiveGoal = function(goal, dropzone) {
			$http.patch(
				'/calendar/api/dashboard/goal/',
				{
					'pk': goal.pk,
					'status': 'archived',
				}
			).then(
				function(response) {
					dropzone.goals.splice(dropzone.goals.indexOf(goal), 1);
				}
			)
		}

		$scope.retreatGoal = function(goal, dropzone) {
			$http.patch(
				'/calendar/api/dashboard/goal/',
				{
					'pk': goal.pk,
					'status': dropzone.prevCol,
				}
			).then(
				function(response) {
					dropzone.goals.splice(dropzone.goals.indexOf(goal), 1);
					$scope.dropzones[dropzone.prevCol].goals.unshift(goal);
				}
			)
		}
		$scope.deleteGoal = function(task, dropzone) {
			var result = confirm('Delete task "' + task.name + '"?');
			if (result) {
				$http.delete(
					'/calendar/api/dashboard/goal/' + task.pk + '/',
					{
						'pk': task.pk,
					}
				).then(
					function(response) {
						dropzone.goals.splice(dropzone.goals.indexOf(task), 1);
					}
				)
			}
		}


		$scope.advanceTask = function(goal, task, dropzone) {
			$http.patch(
				'/calendar/api/dashboard/goal/' + goal.pk + '/tasks/',
				{
					'pk': task.pk,
					'status': dropzone.nextCol,
				}
			).then(
				function(response) {
					goal.dropzones[dropzone.key].tasks.splice(
						goal.dropzones[dropzone.key].tasks.indexOf(task), 1);
					goal.dropzones[dropzone.nextCol].tasks.unshift(task);
				}
			)
		}


		$scope.retreatTask = function(goal, task, dropzone) {$http.patch(
				'/calendar/api/dashboard/goal/' + goal.pk + '/tasks/',
				{
					'pk': task.pk,
					'status': dropzone.prevCol,
				}
			).then(
				function(response) {
					goal.dropzones[dropzone.key].tasks.splice(
						goal.dropzones[dropzone.key].tasks.indexOf(task), 1);
					goal.dropzones[dropzone.prevCol].tasks.unshift(task);
				}
			)
		}

		$scope.dropzones = {
            todo: {
            	key: "todo",
            	displayName: "To Do", 
            	prevCol: null,
            	nextCol: "doing",
            	goals: [],
           	},
            doing: {
            	key: "doing",
            	displayName: "Doing", 
            	prevCol: "todo",
            	nextCol: "done",
            	goals: [],
           	},
            done: {
            	key: "done",
            	displayName: "Done", 
            	prevCol: "doing",
            	nextCol: null,
            	goals: [],
           	}
	    }

	    $scope.setGoal = function(goal) {
	    	goal.dropzones = {
	            todo: {
	            	key: "todo",
	            	displayName: "To Do", 
	            	prevCol: null,
	            	nextCol: "doing",
	            	tasks: [],
	           	},
	            doing: {
	            	key: "doing",
	            	displayName: "Doing", 
	            	prevCol: "todo",
	            	nextCol: "done",
	            	tasks: [],
	           	},
	            done: {
	            	key: "done",
	            	displayName: "Done", 
	            	prevCol: "doing",
	            	nextCol: null,
	            	tasks: [],
	           	}
	        }
	        angular.forEach(goal.todo, function(task, idx){
	        	goal.dropzones.todo.tasks.push(task);
	        });
	        angular.forEach(goal.doing, function(task, idx){
	        	goal.dropzones.doing.tasks.push(task);
	        });
	        angular.forEach(goal.done, function(task, idx){
	        	goal.dropzones.done.tasks.push(task);
	        });
	    }

		$http.get('/calendar/api/dashboard/').then(
			function (response) {
				$scope.day = response.data.day;
				$scope.events = response.data.events;
				$scope.todo = response.data.goals.todo;
				$scope.doing = response.data.goals.doing;
				$scope.done = response.data.goals.done;
				$scope.time_options = response.data.time_options;

				angular.forEach($scope.todo, function(goal, idx){
					$scope.setGoal(goal);
					$scope.dropzones.todo.goals.push(goal);
				});
				angular.forEach($scope.doing, function(goal, idx){
					$scope.setGoal(goal);
					$scope.dropzones.doing.goals.push(goal);
				});
				angular.forEach($scope.done, function(goal, idx){
					$scope.setGoal(goal);
					$scope.dropzones.done.goals.push(goal);
				});

			    $scope.$watch('dropzones', function(model) {
			        $scope.modelAsJson = angular.toJson(model, true);
			    }, true);
			}
		);
	}
);

angular.bootstrap(document.getElementById("dashboardModule"), ['dashboardModule']);

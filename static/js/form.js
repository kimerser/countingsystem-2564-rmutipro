$(document).ready(function () {

	$('form').on('submit', function (event) {
		console.log( $('#facId').val());
		$.ajax({
			data: {
				name: $('#facId').val()
				// email: $('#emailInput').val()
			},
			type: 'POST',
			url: '/insert_fac'
		})
			.done(function (data) {

				if (data.error) {
					$('#errorAlert').text(data.error).show();
					$('#successAlert').hide();
				}
				else {
					$('#successAlert').text(data.name).show();
					$('#errorAlert').hide();
				}

			});

		event.preventDefault();

	});

});
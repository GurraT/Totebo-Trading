$(document).ready(function ()
{
	$(".dropdown-trigger").dropdown();
	$('.datepicker').datepicker(
	{
		format: "dd mmmm, yyyy",
		yearRange: 3,
		showClearBtn: true,
		i18n:
		{
			done: "Select"
		}
	});
});
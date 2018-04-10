$(document).ready(function()
{
  $('form textarea[maxlength]').on('keyup', function()
  {
    e_len = $(this).val().trim().length
    e_min_len = Number($(this).attr('maxlength'))
    message = e_min_len > e_len ? '' : e_min_len + ' characters minimum'
    this.setCustomValidity(message)
  })
})
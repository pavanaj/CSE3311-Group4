$(document).ready(function()
{
  $('form textarea[minlength]').on('keyup', function()
  {
    e_len = $(this).val().trim().length
    e_min_len = Number($(this).attr('minlength'))
    message = e_min_len <= e_len ? '' : e_min_len + ' characters minimum'
    this.setCustomValidity(message)
  })
})
$('#myTabs a').click(function (e) {
  e.preventDefault()
  $(this).tab('show')
})

/*
$('#myTabs a[href="#foil"]').tab('show') // Select tab by name
$('#myTabs a:first').tab('show') // Select first tab
$('#myTabs a:last').tab('show') // Select last tab
$('#myTabs li:eq(2) a').tab('show') // Select third tab (0-indexed)
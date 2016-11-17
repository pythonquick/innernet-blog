var clickbox = document.getElementById('clickbox');
clickbox.addEventListener('mousedown', function(e) {
    var buttonSide = e.button === 0 ? 'left' : 'right';
    alert(buttonSide + '-clicked the ' + e.target.nodeName + ' tag');
});
clickbox.addEventListener('contextmenu', function(e) {
    e.preventDefault();
});


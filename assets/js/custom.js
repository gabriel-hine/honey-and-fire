/*
	Honey & Fire — Custom JS
	Repertoire tab switching + search
*/

(function($) {

	var activeTab = 'all';

	// Repertoire tabs
	$('.repertorio-tabs .tab').on('click', function() {
		activeTab = $(this).data('category');

		$('.repertorio-tabs .tab').removeClass('active');
		$(this).addClass('active');

		// Clear search when switching tabs
		$('#repertorio-search').val('');

		if (activeTab === 'all') {
			$('.repertorio-category').hide();
			$('.repertorio-all').show();
			$('.repertorio-all .song-list li').show();
		} else {
			$('.repertorio-all').hide();
			$('.repertorio-category').hide();
			$('.repertorio-category[data-category="' + activeTab + '"]').show();
			$('.repertorio-category .song-list li').show();
		}

		$('.search-stat').hide();
	});

	// Build the "all" unified list from individual categories
	var $grid = $('.repertorio-grid');
	var allSongs = [];
	$('.repertorio-category .song-list li').each(function() {
		allSongs.push($(this).clone());
	});

	var $allDiv = $('<div class="repertorio-all"><ul class="song-list song-list-all"></ul></div>');
	var $allList = $allDiv.find('.song-list');
	$.each(allSongs, function(i, $li) {
		$allList.append($li);
	});
	$grid.prepend($allDiv);

	// Hide individual categories by default (start with "Tutti")
	$('.repertorio-category').hide();

	// Search
	$('#repertorio-search').on('input', function() {
		var query = $(this).val().toLowerCase().trim();
		var $stat = $('.search-stat');

		if (!query) {
			// Show all, restore tab view
			$('.repertorio-tabs .tab.active').trigger('click');
			$stat.hide();
			return;
		}

		// When searching, show all songs in flat list
		$('.repertorio-category').hide();
		$('.repertorio-all').show();

		var count = 0;
		$('.repertorio-all .song-list li').each(function() {
			var title = $(this).find('.song-title').text().toLowerCase();
			var artist = $(this).find('.song-artist').text().toLowerCase();
			if (title.indexOf(query) !== -1 || artist.indexOf(query) !== -1) {
				$(this).show();
				count++;
			} else {
				$(this).hide();
			}
		});

		$stat.text(count + ' risultat' + (count === 1 ? 'o' : 'i')).show();
	});

	// Clear search
	$('#repertorio-clear').on('click', function() {
		$('#repertorio-search').val('');
		$('.search-stat').hide();
		$('.repertorio-tabs .tab.active').trigger('click');
	});

	// Member photo placeholders — insert initials
	$('.member-photo.placeholder').each(function() {
		var initial = $(this).data('initial');
		if (initial) {
			$(this).text(initial);
		}
	});

})(jQuery);

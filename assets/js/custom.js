/*
	Honey & Fire — Custom JS
	Multi-select repertoire tabs + search
*/

(function($) {

	var $tabs = $('.repertorio-tabs .tab');
	var $songs = $('.repertorio-all .song-list-all li');
	var $stat = $('.search-stat');

	function getActiveCategories() {
		var cats = [];
		$tabs.filter('.active').each(function() {
			var c = $(this).data('category');
			if (c !== 'all') cats.push(c);
		});
		return cats;
	}

	function applyFilter() {
		var query = ($('#repertorio-search').val() || '').toLowerCase().trim();
		var activeCats = getActiveCategories();
		var allMode = activeCats.length === 0;

		var visibleCount = 0;
		$songs.each(function() {
			var $song = $(this);
			var songCats = ($song.data('categories') || '').toString().split(' ');
			var title = $song.find('.song-title').text().toLowerCase();
			var artist = $song.find('.song-artist').text().toLowerCase();

			var catMatch = allMode || activeCats.some(function(c) {
				return songCats.indexOf(c) !== -1;
			});
			var queryMatch = !query ||
				title.indexOf(query) !== -1 ||
				artist.indexOf(query) !== -1;

			if (catMatch && queryMatch) {
				$song.show();
				visibleCount++;
			} else {
				$song.hide();
			}
		});

		// Show stat only when filtering
		if (query || activeCats.length > 0) {
			$stat.text(visibleCount + ' brani').show();
		} else {
			$stat.hide();
		}
	}

	// Tab clicks (multi-select toggle, except "Tutti" which clears all)
	$tabs.on('click', function() {
		var $this = $(this);
		var cat = $this.data('category');

		if (cat === 'all') {
			$tabs.removeClass('active');
			$this.addClass('active');
		} else {
			// Toggle this category
			$this.toggleClass('active');
			// Remove "Tutti" if any specific category is active
			var anyActive = $tabs.filter('.active').not('[data-category="all"]').length > 0;
			if (anyActive) {
				$tabs.filter('[data-category="all"]').removeClass('active');
			} else {
				// No specific category active → activate "Tutti"
				$tabs.filter('[data-category="all"]').addClass('active');
			}
		}
		applyFilter();
	});

	// Search input
	$('#repertorio-search').on('input', applyFilter);

	// Member photo placeholders — insert initials
	$('.member-photo.placeholder').each(function() {
		var initial = $(this).data('initial');
		if (initial) {
			$(this).text(initial);
		}
	});

})(jQuery);

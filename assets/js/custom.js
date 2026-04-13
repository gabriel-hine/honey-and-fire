/*
	Honey & Fire — Custom JS
	Single-select repertoire tabs + search
*/

(function($) {

$(function() {

	var $tabs = $('.repertorio-tabs .tab');
	var $allDiv = $('.repertorio-all');
	var $categoryDivs = $('.repertorio-category');
	var $stat = $('.search-stat');

	function getActiveCategory() {
		var $active = $tabs.filter('.active').first();
		return $active.length ? $active.data('category') : 'all';
	}

	function applyFilter() {
		var query = ($('#repertorio-search').val() || '').toLowerCase().trim();
		var cat = getActiveCategory();

		// Show only the relevant container
		if (cat === 'all') {
			$allDiv.show();
			$categoryDivs.hide();
		} else {
			$allDiv.hide();
			$categoryDivs.hide();
			$categoryDivs.filter('[data-category="' + cat + '"]').show();
		}

		// Apply search filter to visible songs
		var $visibleList = (cat === 'all')
			? $allDiv.find('.song-list li')
			: $categoryDivs.filter('[data-category="' + cat + '"]').find('.song-list li');

		var visibleCount = 0;
		$visibleList.each(function() {
			var $li = $(this);
			var title = $li.find('.song-title').text().toLowerCase();
			var artist = $li.find('.song-artist').text().toLowerCase();
			var match = !query || title.indexOf(query) !== -1 || artist.indexOf(query) !== -1;
			if (match) {
				$li.show();
				visibleCount++;
			} else {
				$li.hide();
			}
		});

		if (query) {
			$stat.text(visibleCount + ' brani').show();
		} else {
			$stat.hide();
		}
	}

	// Single-select tab clicks
	$tabs.on('click', function() {
		$tabs.removeClass('active');
		$(this).addClass('active');
		applyFilter();
	});

	// Search input
	$('#repertorio-search').on('input', applyFilter);

	// Mobile hamburger menu toggle
	var $menuToggle = $('#menu-toggle');
	var $headerNav = $('#header nav');
	$menuToggle.on('click', function() {
		var open = $menuToggle.toggleClass('open').hasClass('open');
		$headerNav.toggleClass('open', open);
		$menuToggle.attr('aria-expanded', open ? 'true' : 'false');
	});
	// Close menu when a nav link is clicked
	$headerNav.find('a').on('click', function() {
		$menuToggle.removeClass('open').attr('aria-expanded', 'false');
		$headerNav.removeClass('open');
	});

});

})(jQuery);

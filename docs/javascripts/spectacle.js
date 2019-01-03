$(function() {

	// Accordion minimal height
	var height = 400;

	// Launch functionality on hljs elements
	$('.hljs').each(function(){ // do this for each matched item

		// Set items
		var $item = $(this),
			$codebox = $item.find('code');
		
		// Create codebox links wrapper
		var $codeboxLinkWrapper = $('<div>', {
			class: 'codebox-links'
		}).appendTo($item)

		// Create copy to clipboard links
		$('<a>', { 
				class: 'codebox-link copy-to-clipboard hide-on-print'
		}).text('Copy to clipboard').click(function(e){

			// Prevent click default and propagation
			e.preventDefault()
			e.stopPropagation()

			// Get text
			var texto = $codebox.text();

			// Copy to clipboard
			copyToClipboard(texto)

		}).appendTo($codeboxLinkWrapper);

		// // Create print links
		// $('<a>', { 
		// 		class: 'codebox-link print-code hide-on-print'
		// }).text('Print').click(function(e){

		// 	// Prevent click default and propagation
		// 	e.preventDefault()
		// 	e.stopPropagation()

		// 	// Get text
		// 	var texto = $codebox.text();

		// 	// Copy to clipboard
		// 	printElem($codebox);

		// }).appendTo($codeboxLinkWrapper);

		// Accordion
		if ($(this).outerHeight() > height) { // search for <p> in context of current element
			$(this).addClass('accordion close');
			$(this).unbind("click");
			$(this).click(function(){
				var sel = getSelection().toString();
				if(!sel){
					$(this).toggleClass('close open');
				}
			})
		}
	});

	// ScrollMagic controller
	var controller = new ScrollMagic.Controller();

	// Create anchor links
	$('nav a').each(function(){
		var anchor      = $(this).attr('href'),
			linkUrl     = window.location.href.split('#')[0] + anchor,
			$icon       = $('<i>').addClass('fa fa-link').attr('aria-hidden', 'true'),
			$anchorLink = $('<a>').attr('href', anchor).addClass('is-anchor-link hide-on-print'),
			$anchor     = $(anchor).addClass('is-anchor');

		// Create objects on DOM
		$anchorLink.append($icon);
		$anchor.append($anchorLink);

		// Create the scene
		new ScrollMagic.Scene({
			triggerElement: anchor,
			duration: 0,	// the scene should last for a scroll distance of 100px
			offset: 500		// start this scene after scrolling for 50px
		})
		.setClassToggle(anchor, 'active')
		.on('start', function(event){
			window.history.pushState("object or string", "Title", anchor);
			// window.location.hash = anchor;
		})
		.addTo(controller); // assign the scene to the controller
	})

	// Copy text to clipboard
	function copyToClipboard(val) {

		var aux = document.createElement("input");
		aux.setAttribute("value", val);
		document.body.appendChild(aux);
		aux.select();
		document.execCommand("copy");

		document.body.removeChild(aux);
	}

	// Print
	function printElem(elem){
		var mywindow = window.open('', 'PRINT', 'height=800,width=800'),
			content = elem.text();

		mywindow.document.write('<html><head><title>' + document.title  + '</title>');
		mywindow.document.write('</head><body >');
		mywindow.document.write('<h1>' + document.title  + '</h1>');
		mywindow.document.write(content);
		mywindow.document.write('</body></html>');

		mywindow.document.close(); // necessary for IE >= 10
		mywindow.focus(); // necessary for IE >= 10*/

		mywindow.print();
		mywindow.close();

		return true;
	}
	
});
$(function() {
  // $(document).foundation();

  var $sidebar = $('#sidebar');
  if ($sidebar.length) {
    var $docs = $('#docs');
    var $nav = $sidebar.find('nav');

    //
    // Setup sidebar navigation
    var traverse = new Traverse($nav, {
      threshold: 10,
      barOffset: $sidebar.position().top
    });

    $nav.on('update.traverse', function(event, element) {
      $nav.find('section').removeClass('expand');
      var $section = element.parents('section:first');
      if ($section.length) {
        $section.addClass('expand');
      }
    });

    //
    // Bind the drawer layout
    var $drawerLayout = $('.drawer-layout'),
      $drawer = $drawerLayout.find('.drawer'),
      closeDrawer = function() {
        $drawer.removeClass('slide-right slide-left');
        $drawer.find('.drawer-overlay').remove();
        $drawerLayout.removeClass('drawer-open drawer-slide-left-large drawer-slide-right-large');
        return false;
      };

    // Drawer open buttons
    $drawerLayout.find('[data-drawer-slide]').click(function(e) {
      var $this = $(this),
        direction = $this.data('drawer-slide');
      $drawerLayout.addClass('drawer-open');
      $drawer.addClass('slide-' + direction);

      var $overlay = $('<a href="#" class="drawer-overlay"></a>')
      $drawer.append($overlay);
      $overlay.click(closeDrawer);

      return false;
    });

    // Drawer close buttons
    $drawerLayout.find('[data-drawer-close]').click(closeDrawer);
  }
});

/**
 * Creates a new instance of Traverse.
 * @class
 * @fires Traverse#init
 * @param {Object} element - jQuery object to add the trigger to.
 * @param {Object} options - Overrides to the default plugin settings.
 */
function Traverse(element, options) {
  this.$element = element;
  this.options  = $.extend({}, Traverse.defaults, this.$element.data(), options);

  this._init();
}

/**
 * Default settings for plugin
 */
Traverse.defaults = {
  /**
   * Amount of time, in ms, the animated scrolling should take between locations.
   * @option
   * @example 500
   */
  animationDuration: 500,
  /**
   * Animation style to use when scrolling between locations.
   * @option
   * @example 'ease-in-out'
   */
  animationEasing: 'linear',
  /**
   * Number of pixels to use as a marker for location changes.
   * @option
   * @example 50
   */
  threshold: 50,
  /**
   * Class applied to the active locations link on the traverse container.
   * @option
   * @example 'active'
   */
  activeClass: 'active',
  /**
   * Allows the script to manipulate the url of the current page, and if supported, alter the history.
   * @option
   * @example true
   */
  deepLinking: false,
  /**
   * Number of pixels to offset the scroll of the page on item click if using a sticky nav bar.
   * @option
   * @example 25
   */
  barOffset: 0
};

/**
 * Initializes the Traverse plugin and calls functions to get equalizer functioning on load.
 * @private
 */
Traverse.prototype._init = function() {
  var id = this.$element[0].id, // || Foundation.GetYoDigits(6, 'traverse'),
      _this = this;
  this.$targets = $('[data-traverse-target]');
  this.$links = this.$element.find('a');
  this.$element.attr({
    'data-resize': id,
    'data-scroll': id,
    'id': id
  });
  this.$active = $();
  this.scrollPos = parseInt(window.pageYOffset, 10);

  this._events();
};

/**
 * Calculates an array of pixel values that are the demarcation lines between locations on the page.
 * Can be invoked if new elements are added or the size of a location changes.
 * @function
 */
Traverse.prototype.calcPoints = function(){
  var _this = this,
      body = document.body,
      html = document.documentElement;

  this.points = [];
  this.winHeight = Math.round(Math.max(window.innerHeight, html.clientHeight));
  this.docHeight = Math.round(Math.max(body.scrollHeight, body.offsetHeight, html.clientHeight, html.scrollHeight, html.offsetHeight));

  this.$targets.each(function(){
    var $tar = $(this),
        pt = $tar.offset().top; // Math.round($tar.offset().top - _this.options.threshold);
    $tar.targetPoint = pt;
    _this.points.push(pt);
  });
};

/**
 * Initializes events for Traverse.
 * @private
 */
Traverse.prototype._events = function() {
  var _this = this,
      $body = $('html, body'),
      opts = {
        duration: _this.options.animationDuration,
        easing:   _this.options.animationEasing
      };

  $(window).one('load', function(){
    _this.calcPoints();
    _this._updateActive();

    $(this).resize(function(e) {
      _this.reflow();
    }).scroll(function(e) {
      _this._updateActive();
    });
  })

  // this.$element.on('click', 'a[href^="#"]', function(e) { //'click.zf.traverse'
  //     e.preventDefault();
  //     var arrival   = this.getAttribute('href').replace(".", "\\."),
  //         scrollPos = $(arrival).offset().top - _this.options.barOffset; // - _this.options.threshold / 2 - _this.options.barOffset;

  //     $body.stop(true).animate({
  //       scrollTop: scrollPos
  //     }, opts);
  //   });
};

/**
 * Calls necessary functions to update Traverse upon DOM change
 * @function
 */
Traverse.prototype.reflow = function(){
  this.calcPoints();
  this._updateActive();
};

/**
 * Updates the visibility of an active location link,
 * and updates the url hash for the page, if deepLinking enabled.
 * @private
 * @function
 * @fires Traverse#update
 */
 Traverse.prototype._updateActive = function(){
   var winPos = parseInt(window.pageYOffset, 10),
       curIdx;

   if(winPos + this.winHeight === this.docHeight){ curIdx = this.points.length - 1; }
   else if(winPos < this.points[0]){ curIdx = 0; }
   else{
     var isDown = this.scrollPos < winPos,
         _this = this,
         curVisible = this.points.filter(function(p, i){
           return isDown ?
             p <= (winPos + _this.options.barOffset + _this.options.threshold) :
             (p - (_this.options.barOffset + _this.options.threshold)) <= winPos;
            //   p <= (winPos - (offset - _this.options.threshold)) :
            //   (p - (-offset + _this.options.threshold)) <= winPos;
         });
     curIdx = curVisible.length ? curVisible.length - 1 : 0;
   }

   var $prev = this.$active;
   var $next = this.$links.eq(curIdx);
   this.$active.removeClass(this.options.activeClass);
   this.$active = $next.addClass(this.options.activeClass);

   if(this.options.deepLinking){
     var hash = this.$active[0].getAttribute('href');
     if(window.history.pushState){
       window.history.pushState(null, null, hash);
     }else{
       window.location.hash = hash;
     }
   }

   this.scrollPos = winPos;

   // Fire event if the active element was changed
   var changed = $prev[0] !== $next[0];
   if (changed) {
     this.$element.trigger('update.traverse', [this.$active]);
   }
 };

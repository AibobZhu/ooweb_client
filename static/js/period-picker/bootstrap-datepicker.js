/*!
 * bootstrap-datepicker.js v2.1.0 (https://github.com/atmulyana/bootstrap-datetime-week-picker)
 * Modified by AT Mulyana in 2015-2016
 * This project is the modification and improvement of another project
 * at https://github.com/eternicode/bootstrap-datepicker/
 * version 1.6.0 developed by Andrew Rowls + contributors.
 *
 * Copyright 2012 Stefan Petre
 * Improvements by Andrew Rowls
 * Licensed under the Apache License v2.0 (http://www.apache.org/licenses/LICENSE-2.0)
 */(function(factory){
    if (typeof define === "function" && define.amd) {
        define(["jquery"], factory);
    } else if (typeof exports === 'object') {
        factory(require('jquery'));
    } else {
        factory(jQuery);
    }
}(function($, undefined){

    function ISO8601_week_no(dt){
         var tdt = new Date(dt.valueOf());
         var dayn = (dt.getDay() + 6) % 7;
         tdt.setDate(tdt.getDate() - dayn + 3);
         var firstThursday = tdt.valueOf();
         tdt.setMonth(0, 1);
         if (tdt.getDay() !== 4){
             tdt.setMonth(0, 1 + ((4 - tdt.getDay()) + 7) % 7);
         }
         return 1 + Math.ceil((firstThursday - tdt) / 604800000);
    }

	function UTCDate(){
		return new Date(Date.UTC.apply(Date, arguments));
	}
	function UTCToday(){
		var today = new Date();
		return UTCDate(today.getFullYear(), today.getMonth(), today.getDate());
	}
	function isUTCEquals(date1, date2) {
		return (
			date1.getUTCFullYear() === date2.getUTCFullYear() &&
			date1.getUTCMonth() === date2.getUTCMonth() &&
			date1.getUTCDate() === date2.getUTCDate()
		);
	}
	function alias(method){
		return function(){
			return this[method].apply(this, arguments);
		};
	}
	function isValidDate(d) {
		return d && !isNaN(d.getTime());
	}

	function DateArray() {
		var a = [];
		Array.apply(a, arguments);
		a._indexes = {};
		a.__push = a.push;
		$.extend(a, DateArray.__extend);
		return a;
	}
	DateArray.prototype = [];
	DateArray.__extend = {
		get: function(i){
			return this.slice(i)[0];
		},
		contains: function(d){
			var t = d.getTime();
			if (t in this._indexes) return this._indexes[t];
			return -1;
		},
		push: function() {
			for (var i=0; i<arguments.length; i++) {
				var d = arguments[i], t = d.getTime();
				if (!(t in this._indexes)) {
					this.__push(d);
					this._indexes[t] = this.length - 1;
				}
			}
		},
		_fixIndexes: function() {
			this._indexes = {};
			var i = 0;
			while (i < this.length) {
				if (this[i]) this._indexes[this[i].getTime()] = i++;
				else {
					this.splice(i, 1);
					if (i >= this.length) break;
				}
			}
		},
		remove: function(){
			if (typeof arguments[0] == 'number') {
				this.splice(arguments[0], 1);
				this._fixIndexes();
			} else if (arguments[0] instanceof Date) {
				for (var j = 0; j < arguments.length; j++) {
					var i = this._indexes[ arguments[j].getTime() ];
					if (i !== undefined) delete this[i];
				}
				this._fixIndexes();
			}
		},
		replace: function(new_array){
			if (!new_array) return;
			if (!$.isArray(new_array) && !(new_array instanceof DateArray)) new_array = [new_array];
			this.clear();
			this.push.apply(this, new_array);
		},
		clear: function(){
			this.length = 0;
			this._fixIndexes();
		},
		copy: function(){
			var a = new DateArray();
			a.replace(this);
			return a;
		}
	};


	// Picker object
	var Datepicker = function(element, options, cb){
    //console.log("==>Datepicker")
		$(element).data('datepicker', this);
		this._process_options(options);

		this.dates = new DateArray();
		this.viewDate = this.o.defaultViewDate;
		this.focusDate = null;

		this.element = $(element);
		this.isInline = false;
		this.isInput = this.element.is('input');
		this.component = this.element.hasClass('date') ? this.element.find('.add-on, .input-group-addon, .btn') : false;
		this.hasInput = this.component && this.element.find('input').length;
		if (this.component && this.component.length === 0)
			this.component = false;

		this.picker = $(DPGlobal.template);

		// Checking templates and inserting
		if (this._check_template(this.o.templates.leftArrow)) {
			this.picker.find('.prev').html(this.o.templates.leftArrow);
		}
		if (this._check_template(this.o.templates.rightArrow)) {
			this.picker.find('.next').html(this.o.templates.rightArrow);
		}

		this._buildEvents();
		this._attachEvents();

		if (this.isInline){
			this.picker.addClass('datepicker-inline').appendTo(this.element);
		}
		else {
			this.picker.addClass('datepicker-dropdown dropdown-menu');
		}

		if (this.o.rtl){
			this.picker.addClass('datepicker-rtl');
		}

		this.viewMode = this.o.startView;

		if (this.o.calendarWeeks)
			this.picker.find('thead .datepicker-title, tfoot th')
						.attr('colspan', function(i, val){
							return parseInt(val) + 1;
						});

		this._allow_update = false;

		this.setStartDate(this._o.startDate);
		this.setEndDate(this._o.endDate);
		this.setDaysOfWeekDisabled(this.o.daysOfWeekDisabled);
		this.setDaysOfWeekHighlighted(this.o.daysOfWeekHighlighted);
		this.setDatesDisabled(this.o.datesDisabled);

		var tp = this._checkTimePart();
		var $time = this.picker.find('tfoot .time');
		if (tp.hour || tp.minute || tp.second) {
			if (tp.second) { /* all displayed */ }
			else if (tp.minute) $time.find('.second').toggle(false);
			else if (tp.hour) $time.find('.minute, .second').toggle(false);
			$time.find('.ampm').toggle(tp.ampm).data('am', true);
			var $input = $time.find('.hour input[type=text]');
			$input.data('min', tp.hMin);
			$input.data('max', tp.hMax);
			$input = $time.find('.minute input[type=text]');
			$input.data('min', 0);
			$input.data('max', 59);
			$input = $time.find('.second input[type=text]');
			$input.data('min', 0);
			$input.data('max', 59);
			this._time = [0,0,0];
		}
		else $time.closest('tr').toggle(false);
		
		this.fillDow();
		this.fillMonths();

		this._allow_update = true;

		this.update();
	    this.showMode();
	    this.cb = cb;
		if (this.isInline){
			this.show();
		}

	};

    Datepicker.prototype = {
		constructor: Datepicker,

		_resolveViewName: function(view, default_value){
			if (view === 0 || view === 'days' || view === 'month') {
				return 0;
			}
			if (view === 1 || view === 'months' || view === 'year') {
				return 1;
			}
			if (view === 2 || view === 'years' || view === 'decade') {
				return 2;
			}
			if (view === 3 || view === 'decades' || view === 'century') {
				return 3;
			}
			if (view === 4 || view === 'centuries' || view === 'millennium') {
				return 4;
			}
			return default_value === undefined ? false : default_value;
		},

		_check_template: function(tmp){
			try {
				// If empty
				if (tmp === undefined || tmp === "") {
					return false;
				}
				// If no html, everything ok
				if ((tmp.match(/[<>]/g) || []).length <= 0) {
					return true;
				}
				// Checking if html is fine
				var jDom = $(tmp);
				return jDom.length > 0;
			}
			catch (ex) {
				return false;
			}
		},

		_process_options: function(opts){
			// Store raw options for reference
			this._o = $.extend({}, this._o, opts);
			// Processed options
			var o = this.o = $.extend({}, this._o);

			// Check if "de-DE" style date is available, if not language should
			// fallback to 2 letter code eg "de"
			var lang = o.language;
			if (!dates[lang]){
				lang = lang.split('-')[0];
				if (!dates[lang])
					lang = defaults.language;
			}
			o.language = lang;

			// Retrieve view index from any aliases
			o.startView = this._resolveViewName(o.startView, 0);
			o.minViewMode = this._resolveViewName(o.minViewMode, 0);
			o.maxViewMode = this._resolveViewName(o.maxViewMode, 4);

			// Check that the start view is between min and max
			o.startView = Math.min(o.startView, o.maxViewMode);
			o.startView = Math.max(o.startView, o.minViewMode);

			// true, false, or Number > 0
			if (o.multidate !== true){
				o.multidate = Number(o.multidate) || false;
				if (o.multidate !== false)
					o.multidate = Math.max(0, o.multidate);
			}
			o.multidateSeparator = String(o.multidateSeparator);

			o.weekStart %= 7;
			o.weekEnd = (o.weekStart + 6) % 7;

			if (typeof JsSimpleDateFormat == 'function') {
				o.format = new JsSimpleDateFormat(o.format, o.language, true);
				o.format.isLenient = true;
			} else {
			    console.log("  JsSimpleDateFormat:", JsSimpleDateFormat);
				o.format = DPGlobal.parseFormat(o.format);
			}
			if (o.startDate !== -Infinity){
				if (!!o.startDate){
					if (o.startDate instanceof Date)
						o.startDate = this._local_to_utc(this._zero_time(o.startDate));
					else
						o.startDate = DPGlobal.parseDate(o.startDate, o.format, o.language, o.assumeNearbyYear);
				}
				else {
					o.startDate = -Infinity;
				}
			}
			if (o.endDate !== Infinity){
				if (!!o.endDate){
					if (o.endDate instanceof Date)
						o.endDate = this._local_to_utc(this._zero_time(o.endDate));
					else
						o.endDate = DPGlobal.parseDate(o.endDate, o.format, o.language, o.assumeNearbyYear);
				}
				else {
					o.endDate = Infinity;
				}
			}

			o.daysOfWeekDisabled = o.daysOfWeekDisabled||[];
			if (!$.isArray(o.daysOfWeekDisabled))
				o.daysOfWeekDisabled = o.daysOfWeekDisabled.split(/[,\s]*/);
			o.daysOfWeekDisabled = $.map(o.daysOfWeekDisabled, function(d){
				return parseInt(d, 10);
			});

			o.daysOfWeekHighlighted = o.daysOfWeekHighlighted||[];
			if (!$.isArray(o.daysOfWeekHighlighted))
				o.daysOfWeekHighlighted = o.daysOfWeekHighlighted.split(/[,\s]*/);
			o.daysOfWeekHighlighted = $.map(o.daysOfWeekHighlighted, function(d){
				return parseInt(d, 10);
			});

			o.datesDisabled = o.datesDisabled||[];
			if (!$.isArray(o.datesDisabled)) {
				var datesDisabled = [];
				datesDisabled.push(DPGlobal.parseDate(o.datesDisabled, o.format, o.language, o.assumeNearbyYear));
				o.datesDisabled = datesDisabled;
			}
			o.datesDisabled = $.map(o.datesDisabled,function(d){
				return DPGlobal.parseDate(d, o.format, o.language, o.assumeNearbyYear);
			});

			var plc = String(o.orientation).toLowerCase().split(/\s+/g),
				_plc = o.orientation.toLowerCase();
			plc = $.grep(plc, function(word){
				return /^auto|left|right|top|bottom$/.test(word);
			});
			o.orientation = {x: 'auto', y: 'auto'};
			if (!_plc || _plc === 'auto')
				; // no action
			else if (plc.length === 1){
				switch (plc[0]){
					case 'top':
					case 'bottom':
						o.orientation.y = plc[0];
						break;
					case 'left':
					case 'right':
						o.orientation.x = plc[0];
						break;
				}
			}
			else {
				_plc = $.grep(plc, function(word){
					return /^left|right$/.test(word);
				});
				o.orientation.x = _plc[0] || 'auto';

				_plc = $.grep(plc, function(word){
					return /^top|bottom$/.test(word);
				});
				o.orientation.y = _plc[0] || 'auto';
			}
			if (o.defaultViewDate) {
				var year = o.defaultViewDate.year || new Date().getFullYear();
				var month = o.defaultViewDate.month || 0;
				var day = o.defaultViewDate.day || 1;
				o.defaultViewDate = UTCDate(year, month, day);
			} else {
				o.defaultViewDate = UTCToday();
			}
			
			var defaultWeekPicker = {
				separator: ' - ',
				formatWeek: function(startWeekDate, options, $datepicker) {
					return DPGlobal.formatDate(startWeekDate, options.format, options.language, options.weekStart)
					/*var endWeekDate = new Date(startWeekDate.getTime() + 6 * 864e5);
					var start = DPGlobal.formatDate(startWeekDate, options.format, options.language);
					var end   = DPGlobal.formatDate(endWeekDate, options.format, options.language)
					return start + options.weekPicker.separator + end;*/
				},
				getWeekStart: function(weekString, options, $datepicker) {
					return DPGlobal.parseDate(weekString.split(options.weekPicker.separator)[0], options.format, options.language);
				}
			};
			if (o.weekPicker) {
				if (typeof o.weekPicker != 'object'){
				    // o.weekPicker == true
				    o.weekPicker = defaultWeekPicker;
				}else {
				    //o.weekPicker == object
					o.weekPicker.separator = o.weekPicker.separator+'' || defaultWeekPicker.separator;
					if (typeof o.weekPicker.formatWeek != 'function') o.weekPicker.formatWeek = defaultWeekPicker.formatWeek;
					if (typeof o.weekPicker.getWeekStart != 'function') o.weekPicker.getWeekStart = defaultWeekPicker.getWeekStart;
				}
			}else{
			    if (typeof o.weekPicker != 'object'){
			        //o.weekPicker == false
			        o.weekPickerBak = defaultWeekPicker;
			    }
			}

		},
		
		_checkTimePart: function() {
			var ret = {hour:false, minute:false, second:false, ampm:false, hMin:0, hMax:23};
			if (this.o.weekPicker || this.o.multidate || !(this.o.format instanceof JsSimpleDateFormat)) return ret;
			var ltr = JsSimpleDateFormat._ltr, ptn = this.o.format._arPtn;
			for (var i=0; i<ptn.length; i++) {
				if (ptn[i] instanceof ltr.k) { ret.hour = true; ret.hMin = 1; ret.hMax = 24; }
				else if (ptn[i] instanceof ltr.H) { ret.hour = true; }
				else if (ptn[i] instanceof ltr.h) { ret.hour = ret.ampm = true; ret.hMin = 1; ret.hMax = 12; }
				else if (ptn[i] instanceof ltr.K) { ret.hour = ret.ampm = true; ret.hMin = 0; ret.hMax = 11; }
				else if (ptn[i] instanceof ltr.m) ret.minute = true;
				else if (ptn[i] instanceof ltr.s) ret.second = true;
			}
			return ret;
		},
		
		_events: [],
		_secondaryEvents: [],
		_applyEvents: function(evs){
			for (var i=0, el, ch, ev; i < evs.length; i++){
				el = evs[i][0];
				if (evs[i].length === 2){
					ch = undefined;
					ev = evs[i][1];
				}
				else if (evs[i].length === 3){
					ch = evs[i][1];
					ev = evs[i][2];
				}
				el.on(ev, ch);
			}
		},
		_unapplyEvents: function(evs){
			for (var i=0, el, ev, ch; i < evs.length; i++){
				el = evs[i][0];
				if (evs[i].length === 2){
					ch = undefined;
					ev = evs[i][1];
				}
				else if (evs[i].length === 3){
					ch = evs[i][1];
					ev = evs[i][2];
				}
				el.off(ev, ch);
			}
		},
		_buildEvents: function(){
            var events = {
                keyup: $.proxy(function(e){
                    if ($.inArray(e.keyCode, [27, 37, 39, 38, 40, 32, 13, 9]) === -1)
                        this.update();
                }, this),
                keydown: $.proxy(this.keydown, this),
                paste: $.proxy(this.paste, this)
            };

            if (this.o.showOnFocus === true) {
                events.focus = $.proxy(this.show, this);
            }

            if (this.isInput) { // single input
                this._events = [
                    [this.element, events]
                ];
            }
            else if (this.component && this.hasInput) { // component: input + button
                this._events = [
                    // For components that are not readonly, allow keyboard nav
                    [this.element.find('input'), events],
                    [this.component, {
                        click: $.proxy(this.show, this)
                    }]
                ];
            }
			else if (this.element.is('div')){  // inline datepicker
				this.isInline = true;
			}
			else {
				this._events = [
					[this.element, {
						click: $.proxy(this.show, this)
					}]
				];
			}
			this._events.push(
				// Component: listen for blur on element descendants
				[this.element, '*', {
					blur: $.proxy(function(e){
						this._focused_from = e.target;
					}, this)
				}],
				// Input: listen for blur on element
				[this.element, {
					blur: $.proxy(function(e){
						this._focused_from = e.target;
					}, this)
				}]
			);

			if (this.o.immediateUpdates) {
				// Trigger input updates immediately on changed year/month
				this._events.push([this.element, {
					'changeYear changeMonth': $.proxy(function(e){
						this.update(e.date);
					}, this)
				}]);
			}

			this._secondaryEvents = [
				[this.picker, {
					click: $.proxy(this.click, this),
					'mousedown touchstart': $.proxy(this.mousedown, this),
					'mouseup mouseout touchend touchmove': $.proxy(this.mouseup, this)
				}],
				[$(window), {
					resize: $.proxy(this.place, this)
				}],
				[$(document), {
					mousedown: $.proxy(function(e){
						// Clicked outside the datepicker, hide it
						if (!(
							this.element.is(e.target) ||
							this.element.find(e.target).length ||
							this.picker.is(e.target) ||
							this.picker.find(e.target).length ||
							this.picker.hasClass('datepicker-inline')
						)){
							this.hide();
						}
					}, this)
				}]
			];
		},
		_attachEvents: function(){
			this._detachEvents();
			this._applyEvents(this._events);
		},
		_detachEvents: function(){
			this._unapplyEvents(this._events);
		},
		_attachSecondaryEvents: function(){
			this._detachSecondaryEvents();
			this._applyEvents(this._secondaryEvents);
		},
		_detachSecondaryEvents: function(){
			this._unapplyEvents(this._secondaryEvents);
		},
		_trigger: function(event, altdate){
			var date = altdate || this.dates.get(-1),
				local_date = this._utc_to_local(date);

			this.element.trigger({
				type: event,
				date: local_date,
				dates: $.map(this.dates, this._utc_to_local),
				format: $.proxy(function(ix, format){
					if (arguments.length === 0){
						ix = this.dates.length - 1;
						format = this.o.format;
					}
					else if (typeof ix === 'string'){
						format = ix;
						ix = this.dates.length - 1;
					}
					format = format || this.o.format;
					var date = this.dates.get(ix);
					return DPGlobal.formatDate(date, format, this.o.language);
				}, this)
			});
		},

		show: function(){
            var element = this.component ? this.element.find('input') : this.element;
			if (element.attr('readonly') && this.o.enableOnReadonly === false)
				return;
			if (!this.isInline)
				this.picker.appendTo(this.o.container);
			this.place();
			this.picker.show();
			this._attachSecondaryEvents();
			this._trigger('show');
			if ((window.navigator.msMaxTouchPoints || 'ontouchstart' in document) && this.o.disableTouchKeyboard) {
				$(this.element).blur();
			}
			return this;
		},

		hide: function(){
			if (this.isInline)
				return this;
			if (!this.picker.is(':visible'))
				return this;
			this.focusDate = null;
			this.picker.hide().detach();
			this._detachSecondaryEvents();
			this.viewMode = this.o.startView;
			this.showMode();

			if (
				this.o.forceParse &&
				(
					this.isInput && this.element.val() ||
					this.hasInput && this.element.find('input').val()
				)
			)
			//this.setValue();
			if (this.cb){
			    var start_date  = new Date(this.range[0])
			    var end_date    = new Date(this.range[1])
			    //var start_date = this.element[0].parentElement.children[0].value;
			    //var end_date = this.element[0].value;
                this.cb(start_date, end_date);
			}else if (this.hasInput && this.element.find('input'))
				console.log("!!!hide, hasInput:" + this.element.find('input').val())
			else
				console.log("!!!hide, ", this)

			this._trigger('hide');
			return this;
		},

		destroy: function(){
			this.hide();
			this._detachEvents();
			this._detachSecondaryEvents();
			this.picker.remove();
			delete this.element.data().datepicker;
			if (!this.isInput){
				delete this.element.data().date;
			}
			return this;
		},

		paste: function(evt){
			var dateString;
			if (evt.originalEvent.clipboardData && evt.originalEvent.clipboardData.types
				&& $.inArray('text/plain', evt.originalEvent.clipboardData.types) !== -1) {
				dateString = evt.originalEvent.clipboardData.getData('text/plain');
			}
			else if (window.clipboardData) {
				dateString = window.clipboardData.getData('Text');
			}
			else {
				return;
			}
			this.setDate(dateString);
			this.update();
			evt.preventDefault();
		},

		_utc_to_local: function(utc){
			return utc && new Date(utc.getTime() + (utc.getTimezoneOffset()*60000));
		},
		_local_to_utc: function(local){
			return local && new Date(local.getTime() - (local.getTimezoneOffset()*60000));
		},
		_zero_time: function(local){
			return local && new Date(local.getFullYear(), local.getMonth(), local.getDate());
		},
		_zero_utc_time: function(utc){
			return utc && new Date(Date.UTC(utc.getUTCFullYear(), utc.getUTCMonth(), utc.getUTCDate()));
		},
		_weekDates: function(startWeekDate) {
			var weekdates = [], year = startWeekDate.getFullYear(), month = startWeekDate.getMonth(), day = startWeekDate.getDate();
			for (var i=6; i>=0; i--) weekdates.push(this._local_to_utc(new Date(year, month, day+i))); //startWeekDate at the last because it'll be viewDate
			return weekdates;
		},
		_getTime: function() {
			var $time = this.picker.find('tfoot .time');
			var $hour = $time.find('.hour input[type=text]'), $minute = $time.find('.minute input[type=text]'),
				$second = $time.find('.second input[type=text]'), $ampm = $time.find('.ampm');
			var h = 0, m = 0, s = 0;
			if ($hour.length > 0) {
				var min = $hour.data('min');
				h = parseInt($hour.val()) || min;
				if ($ampm.is(':visible')) {
					if (min == 1 && h == 12) h = 0;
					if (!$ampm.data('am')) h += 12;
				}
				else if (min == 1 && h == 24) h = 0;
			}
			if ($minute.length > 0) m = parseInt($minute.val()) || 0;
			if ($second.length > 0) s = parseInt($second.val()) || 0;
			return [h, m, s];
		},
		_setTime: function(h, m, s) {
			var $time = this.picker.find('tfoot .time');
			var $hour = $time.find('.hour input[type=text]'), $minute = $time.find('.minute input[type=text]'),
				$second = $time.find('.second input[type=text]'), $ampm = $time.find('.ampm');
			var ampmText = this.o.format.getDateFormatSymbols().getAmPmStrings();
			if (h === null) {
				$hour.val('');
				$minute.val('');
				$second.val('');
				$ampm.data('am', true);
				$ampm.text(ampmText[0]);
				return;
			}
			var setVal = function($input, x) { x = '0' + x; $input.val(x.substring(x.length - 2)); }
			if ($hour.length > 0) {
				var min = $hour.data('min');
				if ($ampm.is(':visible')) {
					var isAM = h < 12;
					h = h % 12;
					if (min == 1 && h == 0) h = 12;
					$ampm.data('am', isAM);
					$ampm.text( isAM ? ampmText[0] : ampmText[1] );
				}
				else if (min == 1 && h == 0) h = 24;
				setVal($hour, h)
			}
			if ($minute.length > 0) setVal($minute, m);
			if ($second.length > 0) setVal($second, s);
		},

		getDates: function(){
			return $.map(this.dates, this._utc_to_local);
		},

		getUTCDates: function(){
			return $.map(this.dates, function(d){
				return new Date(d);
			});
		},

		getDate: function(){
			return this._utc_to_local(this.getUTCDate());
		},

		getUTCDate: function(){
			var selected_date = this.dates.get(-1);
			if (typeof selected_date !== 'undefined') {
				return new Date(selected_date);
			} else {
				return null;
			}
		},

		clearDates: function(){
			var element;
			if (this.isInput) {
				element = this.element;
				this.viewDate = null
			} else if (this.component) {
				element = this.element.find('input');
			}

			if (element) {
				element.val('');
			}

			this.update();
			this._trigger('changeDate');

			if (this.o.autoclose) {
				this.hide();
			}
		},
		setDates: function(){
            /*
            Arguments: [date, trigger_event] or [start_date, end_date, trigger_event]
            */

            /*
		    let viewDate = null;
		    if(this.o.weekPicker){
		        //when set dates under week mode,  use viewDate instead of the passed date, the viewDate should have been assigned previously
		       if(arguments[0] != null && arguments[0] != ""){
		            arguments[0] = this.viewDate;
		            viewDate = this.viewDate;
		        }
		    }*/
			var args = null;
			if($.isArray(arguments[0])){
			    args = arguments[0]
			    if(args.length > 1){
			        if(typeof(args[args.length - 1]) !== 'boolean'){
                        args.push(true)
			        }
			    }else{
			        if(typeof(args[0]) !== 'boolean'){
			            args.push(true)
			        }
			    }
			}else{
			    args = [arguments,true]
			}
			this.update.apply(this, args);
			this._trigger('changeDate');
			this.setValue();
			/*
			if(viewDate){
			    this.viewDate = viewDate;
			}*/
			return this;
		},

		setUTCDates: function(){
			var args = $.isArray(arguments[0]) ? arguments[0] : arguments;
			this.update.apply(this, $.map(args, this._utc_to_local));
			this._trigger('changeDate');
			this.setValue();
			return this;
		},

		setDate: alias('setDates'),
		setUTCDate: alias('setUTCDates'),
		remove: alias('destroy'),

		setValue: function(){
			var formatted = this.getFormattedDate();
			if (!this.isInput){
				if (this.component){
					this.element.find('input').val(formatted);
				}
			}
			else {
				this.element.val(formatted);
			}
			return this;
		},

		getFormattedDate: function(format){
			if (this.o.weekPicker) {
                /*
				var dates = [];
				for (var i=6; i < this.dates.length; i+=7)
				    dates.push(this.o.weekPicker.formatWeek(this.dates[i], this.o, this.element));
				return dates.join(this.o.multidateSeparator);
                */
                if(this.dates == null || this.dates == ""){
                    return "";
                }
                //TODO: find where this.viewDate is changed to be a string
                //Convert this.viewDate to Date object if it's string
                if(typeof(this.viewDate) == 'string'){
                    let view_date = this.viewDate.split('T')[0];
                    view_date = view_date.replace(/-/g,"/");
                    this.viewDate = new Date(view_date)
                    this.viewDate.setHours(this.viewDate.getHours() + 8);
                }
                let week_str = this.o.weekPicker.formatWeek(this.viewDate, this.o, this.element);
                /*
                if(this.o.weekPicker && week_str != "" && week_str != null){
                    if(this.viewDate.getDay() == 0){
                        //fix the issue about jsSimpleFormat threat sunday of the first day of a week, it causes the weeknumber greater 1 then the real
                        let week1 = week_str.split('第');
                        let week2 = parseInt(week1[week1.length-1].split("周")[0])
                        if(week2 > 1){
                            week = week2-1
                            week_str = week1[0] + "第" + week.toString() + "周"
                        }
                    }
                }*/
				return week_str;
			} else {
				if (format === undefined)
				    format = this.o.format;
				var lang = this.o.language;

				var This = this;
				return $.map(this.dates, function(d){
					if (This._time) {
					    d = new Date(d.getTime());
					    d.setUTCHours.apply(d, This._time);
					}
					return DPGlobal.formatDate(d, format, lang);
				}).join(this.o.multidateSeparator);
			}
		},

		getStartDate: function(){
			return this.o.startDate;
		},

		setStartDate: function(startDate){
			this._process_options({startDate: startDate});
			this.update();
			this.updateNavArrows();
			return this;
		},

		getEndDate: function(){
			return this.o.endDate;
		},

		setEndDate: function(endDate){
      //console.log("##setEndDate :",endDate)
			this._process_options({endDate: endDate});
			this.update();
			this.updateNavArrows();
			return this;
		},

		setDaysOfWeekDisabled: function(daysOfWeekDisabled){
			this._process_options({daysOfWeekDisabled: daysOfWeekDisabled});
			this.update();
			this.updateNavArrows();
			return this;
		},

		setDaysOfWeekHighlighted: function(daysOfWeekHighlighted){
			this._process_options({daysOfWeekHighlighted: daysOfWeekHighlighted});
			this.update();
			return this;
		},

		setDatesDisabled: function(datesDisabled){
			this._process_options({datesDisabled: datesDisabled});
			this.update();
			this.updateNavArrows();
		},

		place: function(){
			if (this.isInline)
				return this;
			var calendarWidth = this.picker.outerWidth(),
				calendarHeight = this.picker.outerHeight(),
				visualPadding = 10,
				container = $(this.o.container),
				windowWidth = container.width(),
				scrollTop = this.o.container === 'body' ? $(document).scrollTop() : container.scrollTop(),
				appendOffset = container.offset();

			var parentsZindex = [];
			this.element.parents().each(function(){
				var itemZIndex = $(this).css('z-index');
				if (itemZIndex !== 'auto' && itemZIndex !== 0) parentsZindex.push(parseInt(itemZIndex));
			});
			var zIndex = Math.max.apply(Math, parentsZindex) + this.o.zIndexOffset;
			var offset = this.component ? this.component.parent().offset() : this.element.offset();
			var height = this.component ? this.component.outerHeight(true) : this.element.outerHeight(false);
			var width = this.component ? this.component.outerWidth(true) : this.element.outerWidth(false);
			var left = offset.left - appendOffset.left,
				top = offset.top - appendOffset.top;

			if (this.o.container !== 'body') {
				top += scrollTop;
			}

			this.picker.removeClass(
				'datepicker-orient-top datepicker-orient-bottom '+
				'datepicker-orient-right datepicker-orient-left'
			);

			if (this.o.orientation.x !== 'auto'){
				this.picker.addClass('datepicker-orient-' + this.o.orientation.x);
				if (this.o.orientation.x === 'right')
					left -= calendarWidth - width;
			}
			// auto x orientation is best-placement: if it crosses a window
			// edge, fudge it sideways
			else {
				if (offset.left < 0) {
					// component is outside the window on the left side. Move it into visible range
					this.picker.addClass('datepicker-orient-left');
					left -= offset.left - visualPadding;
				} else if (left + calendarWidth > windowWidth) {
					// the calendar passes the widow right edge. Align it to component right side
					this.picker.addClass('datepicker-orient-right');
					left += width - calendarWidth;
				} else {
					// Default to left
					this.picker.addClass('datepicker-orient-left');
				}
			}

			// auto y orientation is best-situation: top or bottom, no fudging,
			// decision based on which shows more of the calendar
			var yorient = this.o.orientation.y,
				top_overflow;
			if (yorient === 'auto'){
				top_overflow = -scrollTop + top - calendarHeight;
				yorient = top_overflow < 0 ? 'bottom' : 'top';
			}

			this.picker.addClass('datepicker-orient-' + yorient);
			if (yorient === 'top')
				top -= calendarHeight + parseInt(this.picker.css('padding-top'));
			else
				top += height;

			if (this.o.rtl) {
				var right = windowWidth - (left + width);
				this.picker.css({
					top: top,
					right: right,
					zIndex: zIndex
				});
			} else {
				this.picker.css({
					top: top,
					left: left,
					zIndex: zIndex
				});
			}
			return this;
		},

		_allow_update: true,
		update: function(){
            //console.log("## update")
			if (!this._allow_update)
				return this;

			var oldDates = this.dates.copy(),
				dates = [],
				fromArgs = false;
			trigger_event = true;
			if (arguments.length){
				$.each(arguments, $.proxy(function(i, value){
					if (value instanceof Date){
						date = this._local_to_utc(value);
					    dates.push(date);
					}else if(typeof(value) === 'boolean'){
					    trigger_event = value;
					}

				}, this));
				fromArgs = true;
			}
			else {
				dates = this.isInput
						? this.element.val()
						: this.element.data('date') || this.element.find('input').val();
				if (dates && this.o.multidate) {
					dates = dates.split(this.o.multidateSeparator);
					if (this.o.weekPicker) {
						for (var i=0; i<dates.length; i++) dates[i] = this.o.weekPicker.getWeekStart(dates[i], this.o, this.element);
					}
				} else {
					if (dates && this.o.weekPicker) dates = this.o.weekPicker.getWeekStart(dates, this.o, this.element);
					dates = [dates];
				}
				delete this.element.data().date;
			}

			dates = $.map(dates, $.proxy(function(date){

			    //Fix issue about first day of week, if set to monday, should return monday.
			    let _date = null;
			    //if(this.o.weekPicker && this.viewDate && date != "" && date != null){
			    if(this.o.weekPicker && this.viewDate && (date == "" || date == null)){

                //TODO: find where this.viewDate is changed to be a string
                //Convert this.viewDate to Date object if it's string
                if(this.viewDate instanceof String){
                    let view_date = this.viewDate.split('T')[0];
                    view_date = view_date.replace(/-/g,"/");
                    this.viewDate = new Date(view_date);
                    this.viewDate.setHours(this.viewDate.getHours() + 8);
                }
			        _date = this.viewDate;
			    }else{

			    //TODO: find where this.viewDate is changed to be a string
                //Convert this.viewDate to Date object if it's string
                if(this.viewDate instanceof String){
                    let view_date = this.viewDate.split('T')[0];
                    view_date = view_date.replace(/-/g,"/");
                    this.viewDate = new Date(view_date);
                    this.viewDate.setHours(this.viewDate.getHours() + 8);
                }
				    _date = DPGlobal.parseDate(date, this.o.format, this.o.language, this.o.assumeNearbyYear);
				}
				if (!_date) return null;
				if (this._time) {
					this._time = [_date.getUTCHours(), _date.getUTCMinutes(), _date.getUTCSeconds()];
					_date = UTCDate(_date.getUTCFullYear(), _date.getUTCMonth(), _date.getUTCDate());
				}
				ret =  this.o.weekPicker ? DPGlobal.getWeekStart(_date, this.o.weekStart) : _date;
				return ret;
			}, this));
			dates = $.grep(dates, $.proxy(function(date){
				return (
					!this.dateWithinRange(date) ||
					!date
				);
			}, this), true);
			if (this.o.weekPicker) {
				var dates2 = [];
				for (var i=0; i<dates.length; i++) dates2 = dates2.concat(this._weekDates(dates[i]));
				dates = dates2;
			}
			this.dates.replace(dates);

            if (this.o.weekPicker && this.viewDate != null && this.viewDate != ""){
                ; //this.viewDate should have been refreshed before setValue, if viewDate is not null, should is the assignment from another OODatePicker object
                ;//so needn't refresh viewDate
            }else{
                if (this.dates.length)
                    this.viewDate = new Date(this.dates.get(-1));
                else if (this.viewDate < this.o.startDate)
                    this.viewDate = new Date(this.o.startDate);
                else if (this.viewDate > this.o.endDate)
                    this.viewDate = new Date(this.o.endDate);
                else
                    this.viewDate = this.o.defaultViewDate;
            }
			if (fromArgs){
				// setting date by clicking
				this.setValue();
			}
			else if (dates.length){
				// setting date by typing
				if (String(oldDates) !== String(this.dates))
					this._trigger('changeDate');
			}
			if (!this.dates.length && oldDates.length)
				this._trigger('clearDate');

			this.fill();
			if(trigger_event){
			    this.element.change();
			};
			return this;
		},

		fillDow: function(){
			var dowCnt = this.o.weekStart,
				html = '<tr>';
			if (this.o.calendarWeeks){
				this.picker.find('.datepicker-days .datepicker-switch')
					.attr('colspan', function(i, val){
						return parseInt(val) + 1;
					});
				html += '<th class="cw">&#160;</th>';
			}
			while (dowCnt < this.o.weekStart + 7){
				html += '<th class="dow';
        if ($.inArray(dowCnt, this.o.daysOfWeekDisabled) > -1)
          html += ' disabled';
        html += '">'+dates[this.o.language].daysMin[(dowCnt++)%7]+'</th>';
			}
			html += '</tr>';
			this.picker.find('.datepicker-days thead').append(html);
		},
		
		_getViewRange: function(fnCal){
			var range = [-Infinity, -Infinity], j = 1;
			if (this.range && (this.range[0] !== null || this.range[this.range.length-1] !== null)) {
				j = this.range.length-1;
				range[0] = this.range[0] === null ? -Infinity : fnCal(this.range[0]);
				for (var i=1; i<j; i++) {
					range.splice(i, 0, this.range[i] === null ? -Infinity : fnCal(this.range[i]));
				}
				range[j] = this.range[j] === null ? Infinity : fnCal(this.range[j]);
			}
			range.start = range[0];
			range.end = range[j];
			range.isStart = this.__isRangeStart__ || false;
			range.isEnd = this.__isRangeEnd__ || false;
			return range;
		},
		_setRangeClass: function(classes, range, val) {
			if (val == range.start) classes.push('range-start');
			if (val == range.end) classes.push('range-end');
			if (range.start < val && val < range.end) classes.push('range');
			if ($.inArray(val, range) !== -1) { classes.push('selected'); classes.isSelected = true; }
			if (!classes.isSelected && this.o.disableIfExceedRange && range.end !== -Infinity) {
				if (range.isStart && val > range.end || range.isEnd && val < range.start){ 
          classes.push('disabled');
        }
			}
		},

		fillMonths: function(){
            //console.log("##fillMonths")
            var localDate = this._utc_to_local(this.viewDate);
			var html = '';
			var range = this._getViewRange(
				$.proxy(function(val) {
					var dt = this._utc_to_local(new Date(val));
					return dt.getFullYear() * 100 + dt.getMonth();
				}, this)
			);
				
			var i = 0, y = localDate.getFullYear() * 100;
			while (i < 12){
                var cls = ['month'], m = i + y;
                if (!this.range && localDate.getMonth() === i) {
                    cls.push('focused'); cls.isSelected = true;
                }
                this._setRangeClass(cls, range, m);
                html += '<span class="' + cls.join(' ') + '">' + dates[this.o.language].monthsShort[i++]+'</span>';
            }
            this.picker.find('.datepicker-months td').html(html);
		},

		setRange: function(range){
			if (!range || !range.length)
				delete this.range;
			else {
				this.range = [];
				for (var j=0; j < range.length; j++) {
					if (range[j] == null) {
						this.range.push(null);
					} /*else if (this.o.weekPicker) {
						var d = new Date(range[j]);
						if (this.dates.contains(d) != -1)
						    this.range.push(d.valueOf());
						else {
							var dates = this._weekDates(d);
							for (var i=0; i < dates.length; i++) this.range.push(dates[i].valueOf());
						}
					} */else {
						this.range.push(range[j].valueOf());
					}
				}
			}
			this.fill();
		},

		getClassNames: function(date){
			var cls = [],
				year = this.viewDate.getUTCFullYear(),
				month = this.viewDate.getUTCMonth(),
				today = new Date();
			if (date.getUTCFullYear() < year || (date.getUTCFullYear() === year && date.getUTCMonth() < month)){
				cls.push('old');
			}
			else if (date.getUTCFullYear() > year || (date.getUTCFullYear() === year && date.getUTCMonth() > month)){
				cls.push('new');
			}
			if (this.focusDate && date.valueOf() === this.focusDate.valueOf())
				cls.push('focused');
			// Compare internal UTC date with local today, not UTC today
			if (this.o.todayHighlight &&
				date.getUTCFullYear() === today.getFullYear() &&
				date.getUTCMonth() === today.getMonth() &&
				date.getUTCDate() === today.getDate()){
				cls.push('today');
			}
			if (this.dates.contains(date) !== -1) {
				cls.push('active');
				cls.isSelected = true;
			}
			if (!this.dateWithinRange(date) || this.dateIsDisabled(date)){
				cls.push('disabled');
			}
			if ($.inArray(date.getUTCDay(), this.o.daysOfWeekHighlighted) !== -1){
				cls.push('highlighted');
			}
			return cls;
		},

		_fill_yearsView: function(selector, cssClass, factor, step, currentYear, startYear, endYear, callback){
			var html, view, year, steps, startStep, endStep, thisYear, i, classes, tooltip, before;

			html      = '';
			view      = this.picker.find(selector);
			year      = parseInt(currentYear / factor, 10) * factor;
			startStep = parseInt(startYear / step, 10) * step;
			endStep   = parseInt(endYear / step, 10) * step;
			steps     = $.map(this.dates, function(d){
				return parseInt(d.getUTCFullYear() / step, 10) * step;
			});
			
			var range = this._getViewRange(
				function(val) {
					return parseInt(new Date(val).getFullYear() / step, 10) * step;
				}
			);

			view.find('.datepicker-switch').text(year + '-' + (year + step * 9));

			thisYear = year - step;
			for (i = -1; i < 11; i += 1) {
				classes = [cssClass];
				tooltip = null;

				if (i === -1) {
					classes.push('old');
				} else if (i === 10) {
					classes.push('new');
				}
				if ($.inArray(thisYear, steps) !== -1) {
					classes.push('active');
				}
				if (thisYear < startStep || thisYear > endStep) {
					classes.push('disabled');
				}
        if (thisYear === this.viewDate.getFullYear()) {
				  classes.push('focused');
					classes.isSelected = true;
        }
				this._setRangeClass(classes, range, thisYear);
				
				if (callback !== $.noop) {
					before = callback(new Date(thisYear, 0, 1));
					if (before === undefined) {
						before = {};
					} else if (typeof(before) === 'boolean') {
						before = {enabled: before};
					} else if (typeof(before) === 'string') {
						before = {classes: before};
					}
					if (before.enabled === false) {
						classes.push('disabled');
					}
					if (before.classes) {
						classes = classes.concat(before.classes.split(/\s+/));
					}
					if (before.tooltip) {
						tooltip = before.tooltip;
					}
				}

				html += '<span class="' + classes.join(' ') + '"' + (tooltip ? ' title="' + tooltip + '"' : '') + '>' + thisYear + '</span>';
				thisYear += step;
			}
			view.find('td').html(html);
		},

		fill: function(){
			var d = new Date(this.viewDate),
				year = d.getUTCFullYear(),
				month = d.getUTCMonth(),
				startYear = this.o.startDate !== -Infinity ? this.o.startDate.getUTCFullYear() : -Infinity,
				startMonth = this.o.startDate !== -Infinity ? this.o.startDate.getUTCMonth() : -Infinity,
				endYear = this.o.endDate !== Infinity ? this.o.endDate.getUTCFullYear() : Infinity,
				endMonth = this.o.endDate !== Infinity ? this.o.endDate.getUTCMonth() : Infinity,
				todaytxt = this.o.weekPicker ? dates[this.o.language].thisWeek || dates.en.thisWeek || ''
					: dates[this.o.language].today || dates['en'].today || '',
				nowtxt = dates[this.o.language].now || dates['en'].now || '',
				cleartxt = dates[this.o.language].clear || dates['en'].clear || '',
				titleFormat = dates[this.o.language].titleFormat || dates['en'].titleFormat,
				tooltip,
				before;
			if (isNaN(year) || isNaN(month))
				return;
			this.picker.find('.datepicker-days .datepicker-switch')
						.text(DPGlobal.formatDate(d, titleFormat, this.o.language));
			this.picker.find('tfoot .today')
						.text(todaytxt)
						.toggle(this.o.todayBtn !== false);
			this.picker.find('tfoot .now')
						.text(nowtxt)
						.toggle(this.o.nowBtn !== false && this._time !== undefined);
			this.picker.find('tfoot .clear')
						.text(cleartxt)
						.toggle(this.o.clearBtn !== false);
			this.picker.find('thead .datepicker-title')
						.text(this.o.title)
						.toggle(this.o.title !== '');
			this.updateNavArrows();
			this.fillMonths();
			var prevMonth = UTCDate(year, month-1, 28),
				day = DPGlobal.getDaysInMonth(prevMonth.getUTCFullYear(), prevMonth.getUTCMonth());
			prevMonth.setUTCDate(day);
			prevMonth.setUTCDate(day - (prevMonth.getUTCDay() - this.o.weekStart + 7)%7);
			var nextMonth = new Date(prevMonth);
			if (prevMonth.getUTCFullYear() < 100){
                nextMonth.setUTCFullYear(prevMonth.getUTCFullYear());
            }
			nextMonth.setUTCDate(nextMonth.getUTCDate() + 42);
			nextMonth = nextMonth.valueOf();
			var html = [];
			var clsName;
			var range = this._getViewRange(function(val) { return val; });
			while (prevMonth.valueOf() < nextMonth){
				if (prevMonth.getUTCDay() === this.o.weekStart){
					html.push('<tr>');
					if (this.o.calendarWeeks){
						// ISO 8601: First week contains first thursday.
						// ISO also states week starts on Monday, but we can be more abstract here.
						var
							// Start of current week: based on weekstart/current date
							ws = new Date(+prevMonth + (this.o.weekStart - prevMonth.getUTCDay() - 7) % 7 * 864e5),
							// Thursday of this week
							th = new Date(Number(ws) + (7 + 4 - ws.getUTCDay()) % 7 * 864e5),
							// First Thursday of year, year from thursday
							yth = new Date(Number(yth = UTCDate(th.getUTCFullYear(), 0, 1)) + (7 + 4 - yth.getUTCDay())%7*864e5),
							// Calendar week: ms between thursdays, div ms per day, div 7 days
							calWeek =  (th - yth) / 864e5 / 7 + 1;
						html.push('<td class="cw">'+ calWeek +'</td>');

					}
				}
				clsName = this.getClassNames(prevMonth);
				clsName.push('day');
				this._setRangeClass(clsName, range, prevMonth.valueOf());

				if (this.o.beforeShowDay !== $.noop){
					before = this.o.beforeShowDay(this._utc_to_local(prevMonth));
					if (before === undefined)
						before = {};
					else if (typeof(before) === 'boolean')
						before = {enabled: before};
					else if (typeof(before) === 'string')
						before = {classes: before};
					if (before.enabled === false)
						clsName.push('disabled');
					if (before.classes)
						clsName = clsName.concat(before.classes.split(/\s+/));
					if (before.tooltip)
						tooltip = before.tooltip;
				}
				
				clsName = $.unique(clsName);
				html.push('<td class="'+clsName.join(' ')+'"' + (tooltip ? ' title="'+tooltip+'"' : '') + '>'+prevMonth.getUTCDate() + '</td>');
				tooltip = null;
				if (prevMonth.getUTCDay() === this.o.weekEnd){
					html.push('</tr>');
				}
				prevMonth.setUTCDate(prevMonth.getUTCDate()+1);
			}
			this.picker.find('.datepicker-days tbody').empty().append(html.join(''));
			if (this.o.weekPicker) {
				var This = this;
				var $dayRows = this.picker.find('.datepicker-days tbody tr');
				$dayRows.mouseover(function(e) { //using mouseover, not mouseenter is to adapt disabled dates
					var $tr = $(e.delegateTarget);
          //console.log("  ## mouseover tr:", $tr);
					$tr.find('td').css('background-color', $tr.find('td:hover').css('background-color')); //always sets bgcolor because disabled and enabled date's color are different
					if (!$.contains(e.delegateTarget, e.relatedTarget)) {
						var dt = This._getSelectedDate($tr.find('td.day:first'));
            //console.log("  ## weekMouseEnter:",dt)
						This._trigger('weekMouseEnter', dt);
					}
				});
				$dayRows.mouseout(function(e) {
          //console.log("  ## mouseout")
					if (!$.contains(e.delegateTarget, e.relatedTarget)) {
						var $tr = $(e.delegateTarget);
						$tr.find('td').css('background-color', '');
						var dt = This._getSelectedDate($tr.find('td.day:first'));
						This._trigger('weekMouseLeave', dt);
					}
				});
			}
			if (this._time) {
				if (!this.getUTCDate()) { this._setTime(null); this._time = [0,0,0]; }
				else this._setTime(this._time[0], this._time[1], this._time[2]);
			}

			var monthsTitle = dates[this.o.language].monthsTitle || dates['en'].monthsTitle || 'Months';
			var months = this.picker.find('.datepicker-months')
						.find('.datepicker-switch')
							.text(this.o.maxViewMode < 2 ? monthsTitle : year)
							.end()
						.find('span').removeClass('active');

			$.each(this.dates, function(i, d){
				if (d.getUTCFullYear() === year)
					months.eq(d.getUTCMonth()).addClass('active');
			});

			if (year < startYear || year > endYear){
				months.addClass('disabled');
			}
			if (year === startYear){
				months.slice(0, startMonth).addClass('disabled');
			}
			if (year === endYear){
				months.slice(endMonth+1).addClass('disabled');
			}

			if (this.o.beforeShowMonth !== $.noop){
				var that = this;
				$.each(months, function(i, month){
                    var moDate = new Date(year, i, 1);
                    var before = that.o.beforeShowMonth(moDate);
					if (before === undefined)
						before = {};
					else if (typeof(before) === 'boolean')
						before = {enabled: before};
					else if (typeof(before) === 'string')
						before = {classes: before};
					if (before.enabled === false && !$(month).hasClass('disabled'))
					    $(month).addClass('disabled');
					if (before.classes)
					    $(month).addClass(before.classes);
					if (before.tooltip)
					    $(month).prop('title', before.tooltip);
				});
			}

			// Generating decade/years picker
			this._fill_yearsView(
				'.datepicker-years',
				'year',
				10,
				1,
				year,
				startYear,
				endYear,
				this.o.beforeShowYear
			);

			// Generating century/decades picker
			this._fill_yearsView(
				'.datepicker-decades',
				'decade',
				100,
				10,
				year,
				startYear,
				endYear,
				this.o.beforeShowDecade
			);

			// Generating millennium/centuries picker
			this._fill_yearsView(
				'.datepicker-centuries',
				'century',
				1000,
				100,
				year,
				startYear,
				endYear,
				this.o.beforeShowCentury
			);
		},

        updateNavArrows: function(){
			if (!this._allow_update)
				return;

			var d = new Date(this.viewDate),
				year = d.getUTCFullYear(),
				month = d.getUTCMonth();
			switch (this.viewMode){
				case 0:
					if (this.o.startDate !== -Infinity && year <= this.o.startDate.getUTCFullYear() && month <= this.o.startDate.getUTCMonth()){
						this.picker.find('.prev').css({visibility: 'hidden'});
					}
					else {
						this.picker.find('.prev').css({visibility: 'visible'});
					}
					if (this.o.endDate !== Infinity && year >= this.o.endDate.getUTCFullYear() && month >= this.o.endDate.getUTCMonth()){
						this.picker.find('.next').css({visibility: 'hidden'});
					}
					else {
						this.picker.find('.next').css({visibility: 'visible'});
					}
					break;
				case 1:
				case 2:
				case 3:
				case 4:
					if (this.o.startDate !== -Infinity && year <= this.o.startDate.getUTCFullYear() || this.o.maxViewMode < 2){
						this.picker.find('.prev').css({visibility: 'hidden'});
					}
					else {
						this.picker.find('.prev').css({visibility: 'visible'});
					}
					if (this.o.endDate !== Infinity && year >= this.o.endDate.getUTCFullYear() || this.o.maxViewMode < 2){
						this.picker.find('.next').css({visibility: 'hidden'});
					}
					else {
						this.picker.find('.next').css({visibility: 'visible'});
					}
					break;
			}
    },
		
		_timeChange: function(target, repeat) {
			var $target = $(target);
			var $btnCont = $target.parents('div.spinner-buttons');
			var isArrow = true;
			if ($btnCont.length > 0) {
				var $input = $btnCont.siblings('input[type=text]');
				var val = parseInt($input.val());
				var min = $input.data('min');
				if (isNaN(val)) val = min;
				else if ($target.closest('button').hasClass('up')) {
					var max = $input.data('max');
					if (max > val) val++;
				}
				else if (min < val) val--;
				val = '0' + val;
				$input.val(val.substring(val.length - 2));
			}
			else if ($target.hasClass('ampm')) {
				isArrow = false;
				var texts = this.o.format.getDateFormatSymbols().getAmPmStrings();
				var isAM = $target.data('am');
				$target.text( isAM ? texts[1] : texts[0] );
				$target.data('am', !isAM);
			}
			this._setDate(this.viewDate, 'time');
			var This = this;
			if (repeat && isArrow) this._timepickerTimerID = window.setTimeout(function() { This._timeChange(target, true); }, 100);
			return isArrow;
		},
		
		mousedown: function(e) {
			var $time = $(e.target).closest('th.time');
			if ($time.length == 1) {
				if (this._timepickerTimerID !== undefined) window.clearTimeout(this._timepickerTimerID);
				if (this._timeChange(e.target, false)) {
					var This = this;
					this._timepickerTimerID = window.setTimeout(function() { This._timeChange(e.target, true); }, 1000);
				}
			}
		},
		
		mouseup: function(e) {
			var $time = $(e.target).closest('th.time');
			if ($time.length == 1 && this._timepickerTimerID !== undefined) {
				window.clearTimeout(this._timepickerTimerID);
				delete this._timepickerTimerID;
			}
		},

		click: function(e){
			e.preventDefault();
			e.stopPropagation();

			var target, dir, day, year, month;
			target = $(e.target);

			// Clicked on the switch
			if (target.hasClass('datepicker-switch')){
        //console.log("##click switch")
				this.showMode(1);
			}

			// Clicked on prev or next
			var navArrow = target.closest('.prev, .next');
			if (navArrow.length > 0) {
				dir = DPGlobal.modes[this.viewMode].navStep * (navArrow.hasClass('prev') ? -1 : 1);
				if (this.viewMode === 0){
					this.viewDate = this.moveMonth(this.viewDate, dir);
					this._trigger('changeMonth', this.viewDate);
				} else {
					this.viewDate = this.moveYear(this.viewDate, dir);
					if (this.viewMode === 1){
						this._trigger('changeYear', this.viewDate);
					}
				}
				this.fill();
			}

			// Clicked on today/now button
			if (target.hasClass('today') || target.hasClass('now')){
				this.showMode(-2);
				var opt = this.o.todayBtn;
				if (target.hasClass('now')) {
					opt = this.o.nowBtn;
					var d = new Date();
					this._time = [d.getHours(), d.getMinutes(), d.getSeconds()];
					this._setTime.apply(this, this._time);
				}
				this._setDate(UTCToday(), opt === 'linked' ? null : 'view');
			}

			// Clicked on clear button
			if (target.hasClass('clear')){
				this.clearDates();
			}

			if (!target.hasClass('disabled')){
				// Clicked on a day
				if (target.hasClass('day')){
          //console.log("##click a day on target:",target)
					var oChangePart = {}, dt = this._getSelectedDate(target, oChangePart);
          //console.log("  ## got data:",dt);
					this._setDate(dt);
					if (oChangePart.yearChanged) {
						this._trigger('changeYear', this.viewDate);
					}
					if (oChangePart.monthChanged) {
						this._trigger('changeMonth', this.viewDate);
					}
				}

				// Clicked on a month
				if (target.hasClass('month')) {
					this.viewDate.setUTCDate(1);
					day = 1;
					month = target.parent().find('span').index(target);
					year = this.viewDate.getUTCFullYear();
					this.viewDate.setUTCMonth(month);
					this._trigger('changeMonth', this.viewDate);
					if (this.o.minViewMode === 1){
						this._setDate(UTCDate(year, month, day));
						this.showMode();
					} else {
						this.showMode(-1);
					}
					this.fill();
				}

				// Clicked on a year
				if (target.hasClass('year')
						|| target.hasClass('decade')
						|| target.hasClass('century')) {
					this.viewDate.setUTCDate(1);

					day = 1;
					month = 0;
					year = parseInt(target.text(), 10)||0;
					this.viewDate.setUTCFullYear(year);

					if (target.hasClass('year')){
						this._trigger('changeYear', this.viewDate);
						if (this.o.minViewMode === 2){
							this._setDate(UTCDate(year, month, day));
						}
					}
					if (target.hasClass('decade')){
						this._trigger('changeDecade', this.viewDate);
						if (this.o.minViewMode === 3){
							this._setDate(UTCDate(year, month, day));
						}
					}
					if (target.hasClass('century')){
						this._trigger('changeCentury', this.viewDate);
						if (this.o.minViewMode === 4){
							this._setDate(UTCDate(year, month, day));
						}
					}

					this.showMode(-1);
					this.fill();
				}
			}

			if (this.picker.is(':visible') && this._focused_from){
				$(this._focused_from).focus();
			}
			delete this._focused_from;
            var testdate = $(".datepicker");
            //console.log("!!!clicked ", testdate);
		},

		_getSelectedDate: function($target, oChangePart) {
			oChangePart = oChangePart || {};
			day = parseInt($target.text(), 10)||1;
			year = this.viewDate.getUTCFullYear();
			month = this.viewDate.getUTCMonth();
			if ($target.hasClass('old')){
				if (month === 0){
					month = 11;
					year -= 1;
					oChangePart.monthChanged = true;
					oChangePart.yearChanged = true;
				}
				else {
					month -= 1;
					oChangePart.monthChanged = true;
				}
			}
			else if ($target.hasClass('new')){
				if (month === 11){
					month = 0;
					year += 1;
					oChangePart.monthChanged = true;
					oChangePart.yearChanged = true;
				}
				else {
					month += 1;
					oChangePart.monthChanged = true;
				}
			}
			return UTCDate(year, month, day);
		},

		_toggle_multidate: function(date, which){
			if (!date){
				this.dates.clear();
			} else {
				var ix = this.dates.contains(date);
				if (ix !== -1){
					if ((this.o.multidate === true || this.o.multidate > 1 || this.o.toggleActive) && which != 'time'){
						if (this.o.weekPicker) {
							var weekDates = this._weekDates(DPGlobal.getWeekStart(date, this.o.weekStart));
							this.dates.remove.apply(this.dates, weekDates);
						} else
							this.dates.remove(ix);
					}
				} else {
					if (this.o.multidate === false) this.dates.clear();
					if (this.o.weekPicker) {
						var weekDates = this._weekDates(DPGlobal.getWeekStart(date, this.o.weekStart));
						this.dates.push.apply(this.dates, weekDates);
					}
					else
						this.dates.push(date);
				}

				if (typeof this.o.multidate === 'number') {
					var removed = this.dates.length - (this.o.weekPicker ? this.o.multidate * 7 : this.o.multidate);
					if (removed > 0) this.dates.remove.apply(this.dates, this.dates.slice(0, removed));
				}
				
				if (this._time) this._time = this._getTime();
			}
		},

		_setDate: function(date, which){
            //console.log("##_setDate:",date)
			if (!which || which === 'date' || which == 'time')
				this._toggle_multidate(date && new Date(date), which);
			if (!which || which === 'view')
				this.viewDate = date && new Date(date);

			this.fill();
			this.setValue();
			if (!which || which !== 'view') {
				this._trigger('changeDate');
			}
			var element;
			if (this.isInput){
				element = this.element;
			}
			else if (this.component){
				element = this.element.find('input');
			}
			if (element){
				element.change();
			}
			if (this.o.autoclose && (!which || which === 'date')){
				this.hide();
			}
		},

		moveDay: function(date, dir){
			var newDate = new Date(date);
			newDate.setUTCDate(date.getUTCDate() + dir);

			return newDate;
		},

		moveWeek: function(date, dir){
			return this.moveDay(date, dir * 7);
		},

		moveMonth: function(date, dir){
			if (!isValidDate(date))
				return this.o.defaultViewDate;
			if (!dir)
				return date;
			var new_date = new Date(date.valueOf()),
				day = new_date.getUTCDate(),
				month = new_date.getUTCMonth(),
				mag = Math.abs(dir),
				new_month, test;
			dir = dir > 0 ? 1 : -1;
			if (mag === 1){
				test = dir === -1
					// If going back one month, make sure month is not current month
					// (eg, Mar 31 -> Feb 31 == Feb 28, not Mar 02)
					? function(){
						return new_date.getUTCMonth() === month;
					}
					// If going forward one month, make sure month is as expected
					// (eg, Jan 31 -> Feb 31 == Feb 28, not Mar 02)
					: function(){
						return new_date.getUTCMonth() !== new_month;
					};
				new_month = month + dir;
				new_date.setUTCMonth(new_month);
				// Dec -> Jan (12) or Jan -> Dec (-1) -- limit expected date to 0-11
				if (new_month < 0 || new_month > 11)
					new_month = (new_month + 12) % 12;
			}
			else {
				// For magnitudes >1, move one month at a time...
				for (var i=0; i < mag; i++)
					// ...which might decrease the day (eg, Jan 31 to Feb 28, etc)...
					new_date = this.moveMonth(new_date, dir);
				// ...then reset the day, keeping it in the new month
				new_month = new_date.getUTCMonth();
				new_date.setUTCDate(day);
				test = function(){
					return new_month !== new_date.getUTCMonth();
				};
			}
			// Common date-resetting loop -- if date is beyond end of month, make it
			// end of month
			while (test()){
				new_date.setUTCDate(--day);
				new_date.setUTCMonth(new_month);
			}
			return new_date;
		},

		moveYear: function(date, dir){
			return this.moveMonth(date, dir*12);
		},

		moveAvailableDate: function(date, dir, fn){
			do {
				date = this[fn](date, dir);

				if (!this.dateWithinRange(date))
					return false;

				fn = 'moveDay';
			}
			while (this.dateIsDisabled(date));

			return date;
		},

		weekOfDateIsDisabled: function(date){
			return $.inArray(date.getUTCDay(), this.o.daysOfWeekDisabled) !== -1;
		},

		dateIsDisabled: function(date){
			return (
				this.weekOfDateIsDisabled(date) ||
				$.grep(this.o.datesDisabled, function(d){
					return isUTCEquals(date, d);
				}).length > 0
			);
		},

		dateWithinRange: function(date){
			return date >= this.o.startDate && date <= this.o.endDate;
		},

		keydown: function(e){
			if (!this.picker.is(':visible')){
				if (e.keyCode === 40 || e.keyCode === 27) { // allow down to re-show picker
					this.show();
					e.stopPropagation();
        }
				return;
			}
			var dateChanged = false,
				dir, newViewDate,
				focusDate = this.focusDate || this.viewDate;
			switch (e.keyCode){
				case 27: // escape
					if (this.focusDate){
						this.focusDate = null;
						this.viewDate = this.dates.get(-1) || this.viewDate;
						this.fill();
					}
					else
						this.hide();
					e.preventDefault();
					e.stopPropagation();
					break;
				case 37: // left
				case 38: // up
				case 39: // right
				case 40: // down
					if (!this.o.keyboardNavigation || this.o.daysOfWeekDisabled.length === 7)
						break;
					dir = e.keyCode === 37 || e.keyCode === 38 ? -1 : 1;
          if (this.viewMode === 0) {
  					if (e.ctrlKey){
  						newViewDate = this.moveAvailableDate(focusDate, dir, 'moveYear');

  						if (newViewDate)
  							this._trigger('changeYear', this.viewDate);
  					}
  					else if (e.shiftKey){
  						newViewDate = this.moveAvailableDate(focusDate, dir, 'moveMonth');

  						if (newViewDate)
  							this._trigger('changeMonth', this.viewDate);
  					}
  					else if (e.keyCode === 37 || e.keyCode === 39){
  						newViewDate = this.moveAvailableDate(focusDate, dir, 'moveDay');
  					}
  					else if (!this.weekOfDateIsDisabled(focusDate)){
  						newViewDate = this.moveAvailableDate(focusDate, dir, 'moveWeek');
  					}
          } else if (this.viewMode === 1) {
            if (e.keyCode === 38 || e.keyCode === 40) {
              dir = dir * 4;
            }
            newViewDate = this.moveAvailableDate(focusDate, dir, 'moveMonth');
          } else if (this.viewMode === 2) {
            if (e.keyCode === 38 || e.keyCode === 40) {
              dir = dir * 4;
            }
            newViewDate = this.moveAvailableDate(focusDate, dir, 'moveYear');
          }
					if (newViewDate){
						this.focusDate = this.viewDate = newViewDate;
						this.setValue();
						this.fill();
						e.preventDefault();
					}
					break;
				case 13: // enter
          //console.log("## enter")
					if (!this.o.forceParse)
						break;
					focusDate = this.focusDate || this.dates.get(-1) || this.viewDate;
					if (this.o.keyboardNavigation) {
						this._toggle_multidate(focusDate);
						dateChanged = true;
					}
					this.focusDate = null;
					this.viewDate = this.dates.get(-1) || this.viewDate;
					this.setValue();
					this.fill();
					if (this.picker.is(':visible')){
						e.preventDefault();
						e.stopPropagation();
						if (this.o.autoclose)
							this.hide();
					}
					break;
				case 9: // tab
					this.focusDate = null;
					this.viewDate = this.dates.get(-1) || this.viewDate;
					this.fill();
					this.hide();
					break;
			}
			if (dateChanged){
				if (this.dates.length)
					this._trigger('changeDate');
				else
					this._trigger('clearDate');
				var element;
				if (this.isInput){
					element = this.element;
				}
				else if (this.component){
					element = this.element.find('input');
				}
				if (element){
					element.change();
				}
			}
		},

		showMode: function(dir){
      //console.log("##showModel this:",this)
        if (dir){
            this.viewMode = Math.max(this.o.minViewMode, Math.min(this.o.maxViewMode, this.viewMode + dir));
        }
        this.picker
            .children('div')
            .hide()
            .filter('.datepicker-' + DPGlobal.modes[this.viewMode].clsName)
                .show();
        this.updateNavArrows();
      //console.log("##this.viewModel:",this.viewMode)
      //console.log("##class:",'.datepicker-' + DPGlobal.modes[this.viewMode].clsName)
		}

	};

	var DateRangePicker = function(element, options, cb){
        //console.log("!!!DateRangePicker ")
		$(element).data('datepicker', this);
		this.element = $(element);
		this.inputs = $.map(options.inputs, function(i){
			return i.jquery ? i[0] : i;
		});
		delete options.inputs;

		datepickerPlugin.call($(this.inputs), options,cb)
			.on('changeDate', $.proxy(this.dateUpdated, this));

		this.pickers = $.map(this.inputs, function(i){
			return $(i).data('datepicker');
		});

		if(this.pickers.length > 1){
		    this.pickers[0].__isRangeStart__ = true;
		    this.pickers[this.pickers.length-1].__isRangeEnd__ = true;
		}else{
		    this.pickers[0].__isRangeStart__ = false;
		    this.pickers[0].__isRangeEnd__ = false;
		}
		this.updateDates();
	};

	DateRangePicker.prototype = {
		updateDates: function(){
			this.dates = $.map(this.pickers, function(i){
				var d = i.getUTCDate();
				return d ? d : [null];
			});
			this.updateRanges();
		},
		updateRanges: function(){
			var range = $.map(this.dates, function(d){
				return d ? d.valueOf() : [null];
			});
			$.each(this.pickers, function(i, p){
				p.setRange(range);
			});
		},
		dateUpdated: function(e){
			// `this.updating` is a workaround for preventing infinite recursion
			// between `changeDate` triggering and `setUTCDate` calling.  Until
			// there is a better mechanism.
			if (this.updating)
				return;
			this.updating = true;

			var dp = $(e.target).data('datepicker');

			if (typeof(dp) === "undefined") {
				return;
			}

			var new_date = dp.getUTCDate(),
				i = $.inArray(e.target, this.inputs),
				j = i - 1,
				k = i + 1,
				l = this.inputs.length;
			if (i === -1)
				return;

			// Date being moved earlier/left
			while (j >= 0 && new_date < this.dates[j]){
				this.pickers[j--].setUTCDate(new_date);
			}
			// Date being moved later/right
			while (k < l && new_date > this.dates[k] && this.dates[k] != null){
				this.pickers[k++].setUTCDate(new_date);
			}
			this.updateDates();

			delete this.updating;
		},
		remove: function(){
			$.map(this.pickers, function(p){ p.remove(); });
			delete this.element.data().datepicker;
		}
	};

	function opts_from_el(el, prefix){
		// Derive options from element data-attrs
		var data = $(el).data(),
			out = {}, inkey,
			replace = new RegExp('^' + prefix.toLowerCase() + '([A-Z])');
		prefix = new RegExp('^' + prefix.toLowerCase());
		function re_lower(_,a){
			return a.toLowerCase();
		}
		for (var key in data)
			if (prefix.test(key)){
				inkey = key.replace(replace, re_lower);
				out[inkey] = data[key];
			}
		return out;
	}

	function opts_from_locale(lang){
		// Derive options from locale plugins
		var out = {};
		// Check if "de-DE" style date is available, if not language should
		// fallback to 2 letter code eg "de"
		if (!dates[lang]){
			lang = lang.split('-')[0];
			if (!dates[lang])
				return;
		}
		var d = dates[lang];
		$.each(locale_opts, function(i,k){
			if (k in d)
				out[k] = d[k];
		});
		return out;
	}

	var old = $.fn.datepicker;

	var datepickerPlugin = function(option, cb){
		var args = Array.apply(null, arguments);
		args.shift();
		var internal_return;
		this.each(function(){
			var $this = $(this),
				data = $this.data('datepicker'),
				options = typeof option === 'object' && option;
			if (!data){
                console.log(" for data is null");
				var elopts = opts_from_el(this, 'date'),
					// Preliminary otions
					xopts = $.extend({}, defaults, elopts, options),
					locopts = opts_from_locale(xopts.language),
					// Options priority: js args, data-attrs, locales, defaults
					opts = $.extend({}, defaults, locopts, elopts, options);
				if ($this.hasClass('input-daterange') || opts.inputs){
					$.extend(opts, {
						inputs: opts.inputs || $this.find('input').toArray()
					});
					data = new DateRangePicker(this, opts,cb);
				}
				else {
					data = new Datepicker(this, opts, cb);
				}
				$this.data('datepicker', data);
			}
			if (typeof option === 'string' && typeof data[option] === 'function'){
				internal_return = data[option].apply(data, args);
			}
		});

		if (
			internal_return === undefined ||
			internal_return instanceof Datepicker ||
			internal_return instanceof DateRangePicker
		)
		return this;

		if (this.length > 1)
			throw new Error('Using only allowed for the collection of a single element (' + option + ' function)');
		else
			return internal_return;
	};

	$.fn.datepicker = datepickerPlugin;

	var defaults = $.fn.datepicker.defaults = {
		assumeNearbyYear: false,
		autoclose: false,
		beforeShowDay: $.noop,
		beforeShowMonth: $.noop,
		beforeShowYear: $.noop,
		beforeShowDecade: $.noop,
		beforeShowCentury: $.noop,
		calendarWeeks: false,
		clearBtn: false,
		toggleActive: false,
		daysOfWeekDisabled: [],
		daysOfWeekHighlighted: [],
		datesDisabled: [],
		endDate: Infinity,
		forceParse: true,
		format: (typeof JsSimpleDateFormat == 'function') ? 'MM/dd/yyyy' : 'mm/dd/yyyy',
		keyboardNavigation: true,
		language: 'zh',
		minViewMode: 0,
		maxViewMode: 4,
		multidate: false,
		multidateSeparator: ',',
		orientation: "auto",
		rtl: false,
		startDate: -Infinity,
		startView: 0,
		todayBtn: false,
		nowBtn: false,
		todayHighlight: false,
		weekStart: 0,
		disableTouchKeyboard: false,
		enableOnReadonly: true,
		showOnFocus: true,
		zIndexOffset: 10,
		container: 'body',
		immediateUpdates: false,
		title: '',
		templates: {
			leftArrow: '&laquo;',
			rightArrow: '&raquo;'
		},
		weekPicker: false,
		disableIfExceedRange: false,
	};
	var locale_opts = $.fn.datepicker.locale_opts = [
		'format',
		'rtl',
		'weekStart'
	];
	$.fn.datepicker.Constructor = Datepicker;
	var dates = $.fn.datepicker.dates = {
		en: {
			days: ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
			daysShort: ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
			daysMin: ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"],
			months: ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
			monthsShort: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
			today: "Today",
			now: "Now",
			thisWeek: "This Week",
			clear: "Clear",
			titleFormat: "MM yyyy"
		},
		zh: {
			days: ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"],
			daysShort: ["周日", "周一", "周二", "周三", "周四", "周五", "周六"],
			daysMin: ["日", "一", "二", "三", "四", "五", "六"],
			months: ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"],
			monthsShort: ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"],
			today: "今日",
			now: "现在",
			thisWeek: "本周",
			clear: "清除",
			titleFormat: "yyyy MM"
		}
	};

	var DPGlobal = {
		modes: [
			{
				clsName: 'days',
				navFnc: 'Month',
				navStep: 1
			},
			{
				clsName: 'months',
				navFnc: 'FullYear',
				navStep: 1
			},
			{
				clsName: 'years',
				navFnc: 'FullYear',
				navStep: 10
			},
			{
				clsName: 'decades',
				navFnc: 'FullDecade',
				navStep: 100
			},
			{
				clsName: 'centuries',
				navFnc: 'FullCentury',
				navStep: 1000
		}],
		isLeapYear: function(year){
			return (((year % 4 === 0) && (year % 100 !== 0)) || (year % 400 === 0));
		},
		getDaysInMonth: function(year, month){
			return [31, (DPGlobal.isLeapYear(year) ? 29 : 28), 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month];
		},
		validParts: /dd?|DD?|mm?|MM?|yy(?:yy)?/g,
		nonpunctuation: /[^ -\/:-@\u5e74\u6708\u65e5\[-`{-~\t\n\r]+/g,
		parseFormat: function(format){
			if (typeof format.toValue === 'function' && typeof format.toDisplay === 'function')
                return format;
            // IE treats \0 as a string end in inputs (truncating the value),
			// so it's a bad format delimiter, anyway
			var separators = format.replace(this.validParts, '\0').split('\0'),
				parts = format.match(this.validParts);
			if (!separators || !separators.length || !parts || parts.length === 0){
				throw new Error("Invalid date format.");
			}
			return {separators: separators, parts: parts};
		},
		_parseDateDiff: function(date){
			if (/^[\-+]\d+[dmMwy]([\s,]+[\-+]\d+[dmwy])*$/.test(date)){
				var part_re = /([\-+]\d+)([dmwy])/,
					parts = date.match(/([\-+]\d+)([dmwy])/g),
					fn_map = {
						d: 'moveDay',
						m: 'moveMonth',
						w: 'moveWeek',
						y: 'moveYear'
					},
					part, dir, i, fn;
				for (i=0; i < parts.length; i++){
					part = part_re.exec(parts[i]);
					dir = parseInt(part[1]);
					fn = fn_map[part[2]];
					date = Datepicker.prototype[fn](date, dir);
				}
				return UTCDate(date.getUTCFullYear(), date.getUTCMonth(), date.getUTCDate(), 0, 0, 0);
			}
			return null;
		},
		parseDate: function(date, format, language, assumeNearby){
			if (!date)
				return undefined;
			if (date instanceof Date)
				return date;
			if (typeof format === 'string')
				format = DPGlobal.parseFormat(format);
			if (format.toValue)
                return format.toValue(date, format, language);
            var part_re = /([\-+]\d+)([dmwy])/,
				parts = date.match(/([\-+]\d+)([dmwy])/g),
				fn_map = {
					d: 'moveDay',
					m: 'moveMonth',
					w: 'moveWeek',
					y: 'moveYear'
				},
				dateAliases = {
					yesterday: '-1d',
					today: '+0d',
					tomorrow: '+1d'
				},
				part, i;
			if (date = DPGlobal._parseDateDiff(new Date())) return date;

			if (typeof dateAliases[date] !== 'undefined') {
				if (date = DPGlobal._parseDateDiff(dateAliases[date])) return date;
			}

			var parts = date && date.match(this.nonpunctuation) || [];
			date = new Date();

			function applyNearbyYear(year, threshold){
				if (threshold === true)
					threshold = 10;

				// if year is 2 digits or less, than the user most likely is trying to get a recent century
				if (year < 100){
					year += 2000;
					// if the new year is more than threshold years in advance, use last century
					if (year > ((new Date()).getFullYear()+threshold)){
						year -= 100;
					}
				}

				return year;
			}

			var parsed = {},
				setters_order = ['yyyy', 'yy', 'M', 'MM', 'm', 'mm', 'd', 'dd'],
				setters_map = {
					yyyy: function(d,v){
						return d.setUTCFullYear(assumeNearby ? applyNearbyYear(v, assumeNearby) : v);
					},
					yy: function(d,v){
						return d.setUTCFullYear(assumeNearby ? applyNearbyYear(v, assumeNearby) : v);
					},
					m: function(d,v){
						if (isNaN(d))
							return d;
						v -= 1;
						while (v < 0) v += 12;
						v %= 12;
						d.setUTCMonth(v);
						while (d.getUTCMonth() !== v)
							d.setUTCDate(d.getUTCDate()-1);
						return d;
					},
					d: function(d,v){
						return d.setUTCDate(v);
					}
				},
				val, filtered;
			setters_map['M'] = setters_map['MM'] = setters_map['mm'] = setters_map['m'];
			setters_map['dd'] = setters_map['d'];
			date = UTCToday();
			var fparts = format.parts.slice();
			// Remove noop parts
			if (parts.length !== fparts.length){
				fparts = $(fparts).filter(function(i,p){
					return $.inArray(p, setters_order) !== -1;
				}).toArray();
			}
			// Process remainder
			function match_part(){
				var m = this.slice(0, parts[i].length),
					p = parts[i].slice(0, m.length);
				return m.toLowerCase() === p.toLowerCase();
			}
			if (parts.length === fparts.length){
				var cnt;
				for (i=0, cnt = fparts.length; i < cnt; i++){
					val = parseInt(parts[i], 10);
					part = fparts[i];
					if (isNaN(val)){
						switch (part){
							case 'MM':
								filtered = $(dates[language].months).filter(match_part);
								val = $.inArray(filtered[0], dates[language].months) + 1;
								break;
							case 'M':
								filtered = $(dates[language].monthsShort).filter(match_part);
								val = $.inArray(filtered[0], dates[language].monthsShort) + 1;
								break;
						}
					}
					parsed[part] = val;
				}
				var _date, s;
				for (i=0; i < setters_order.length; i++){
					s = setters_order[i];
					if (s in parsed && !isNaN(parsed[s])){
						_date = new Date(date);
						setters_map[s](_date, parsed[s]);
						if (!isNaN(_date))
							date = _date;
					}
				}
			}
			return date;
		},
		formatDate: function(date, format, language){

		    var o = this.o;
			if (!date)
				return '';
			if (typeof format.toPattern === 'function')
			    format = format.toPattern();
			    format = format.replace('MMMM','MM')
			    /*format = "yyyy MM dd"*/
			if (typeof format === 'string' )
				format = DPGlobal.parseFormat(format);

			if (format.toDisplay)
                return format.toDisplay(date, format, language);
            var val = {
                d: date.getUTCDate(),
				D: dates[language].daysShort[date.getUTCDay()],
				DD: dates[language].days[date.getUTCDay()],
				m: date.getUTCMonth() + 1,
				M: dates[language].monthsShort[date.getUTCMonth()],
				MM: dates[language].months[date.getUTCMonth()],
				yy: date.getUTCFullYear().toString().substring(2),
				yyyy: date.getUTCFullYear()
			};
			if (language === 'zh'){
			    val.dd = (val.d < 10 ? '0' : '') + val.d;
			    val.mm = (val.m < 10 ? '0' : '') + val.m;
			    val['d'] = val['d'] + '日';
			    val['yyyy'] = val['yyyy'] + '年';
			}else{
			    val.dd = (val.d < 10 ? '0' : '') + val.d;
			    val.mm = (val.m < 10 ? '0' : '') + val.m;
			};
			date = [];
			var seps = $.extend([], format.separators);
			for (var i=0, cnt = format.parts.length; i <= cnt; i++){
				if (seps.length)
					date.push(seps.shift());
				date.push(val[format.parts[i]]);
			}
			return date.join('');
		},
		getWeekStart: function(date, startDay) {
			if (typeof(startDay) != 'number' || startDay < 0 || startDay > 6) startDay = 0;
			date = new Date(date.getFullYear(), date.getMonth(), date.getDate());
			var currentDay = date.getDay(), dec = (currentDay >= startDay ? 0 : 7) + currentDay - startDay;
			return Datepicker.prototype._local_to_utc(new Date(date.getTime() - dec * 864e5));
		},
		headTemplate: '<thead>'+
			              '<tr>'+
			                '<th colspan="7" class="datepicker-title"></th>'+
			              '</tr>'+
							'<tr>'+
								'<th class="prev">&laquo;</th>'+
								'<th colspan="5" class="datepicker-switch"></th>'+
								'<th class="next">&raquo;</th>'+
							'</tr>'+
						'</thead>',
		contTemplate: '<tbody><tr><td colspan="7"></td></tr></tbody>',
		footDaysTemplate: '<tfoot>'+
							'<tr>'+
								'<th colspan="7" class="time">'+
									'<div class="hour">'+
										'<div class="colon"></div>'+
										'<input type="text" class="form-control time-input" readonly maxlength="2" />'+
										'<div class="spinner-buttons input-group-btn btn-group-vertical">'+
											'<button type="button" class="btn btn-default btn-xs up">'+
												'<i class="glyphicon glyphicon-chevron-up"></i>'+
											'</button>'+
											'<button type="button" class="btn btn-default btn-xs down">'+
												'<i class="glyphicon glyphicon-chevron-down"></i>'+
											'</button>'+
										'</div>'+
									'</div>'+
									'<div class="minute">'+
										'<div class="colon">:</div>'+
										'<input type="text" class="form-control time-input" readonly maxlength="2" />'+
										'<div class="spinner-buttons input-group-btn btn-group-vertical">'+
											'<button type="button" class="btn btn-default btn-xs up">'+
												'<i class="glyphicon glyphicon-chevron-up"></i>'+
											'</button>'+
											'<button type="button" class="btn btn-default btn-xs down">'+
												'<i class="glyphicon glyphicon-chevron-down"></i>'+
											'</button>'+
										'</div>'+
									'</div>'+
									'<div class="second">'+
										'<div class="colon">:</div>'+
										'<input type="text" class="form-control time-input" readonly maxlength="2" />'+
										'<div class="spinner-buttons input-group-btn btn-group-vertical">'+
											'<button type="button" class="btn btn-default btn-xs up">'+
												'<i class="glyphicon glyphicon-chevron-up"></i>'+
											'</button>'+
											'<button type="button" class="btn btn-default btn-xs down">'+
												'<i class="glyphicon glyphicon-chevron-down"></i>'+
											'</button>'+
										'</div>'+
									'</div>'+
									'<button type="button" class="btn btn-default btn-xs btn-mini ampm">AM</button>'+
								'</th>'+
							'</tr><tr>'+
								'<th colspan="7">'+
									'<span class="today"></span>'+
									'<span class="now"></span>'+
									'<span class="clear"></span>'+
								'</th>'+
							'</tr>'+
						'</tfoot>',
		footTemplate: '<tfoot>'+
							'<tr>'+
								'<th colspan="7">'+
									'<span class="today"></span>'+
									'<span class="clear"></span>'+
								'</th>'+
							'</tr>'+
						'</tfoot>'
	};
	DPGlobal.template = '<div class="datepicker">'+
							'<div class="datepicker-days">'+
								'<table class=" table-condensed">'+
									DPGlobal.headTemplate+
									'<tbody></tbody>'+
									DPGlobal.footDaysTemplate+
								'</table>'+
							'</div>'+
							'<div class="datepicker-months">'+
								'<table class="table-condensed">'+
									DPGlobal.headTemplate+
									DPGlobal.contTemplate+
									DPGlobal.footTemplate+
								'</table>'+
							'</div>'+
							'<div class="datepicker-years">'+
								'<table class="table-condensed">'+
									DPGlobal.headTemplate+
									DPGlobal.contTemplate+
									DPGlobal.footTemplate+
								'</table>'+
							'</div>'+
							'<div class="datepicker-decades">'+
								'<table class="table-condensed">'+
									DPGlobal.headTemplate+
									DPGlobal.contTemplate+
									DPGlobal.footTemplate+
								'</table>'+
							'</div>'+
							'<div class="datepicker-centuries">'+
								'<table class="table-condensed">'+
									DPGlobal.headTemplate+
									DPGlobal.contTemplate+
									DPGlobal.footTemplate+
								'</table>'+
							'</div>'+
						'</div>';
	
	if (typeof JsSimpleDateFormat == 'function') {
		DPGlobal.setFormatSymbols = function(format, language) {
			var symbols = new JsDateFormatSymbols();
			var words = dates[language];
			symbols.setAmPmStrings(['AM','PM']);
			symbols.setEras(['AD','BC']);
			symbols.setMonths(words.months);
			symbols.setShortMonths(words.monthsShort);
			symbols.setShortWeekdays(words.daysShort);
			symbols.setWeekdays(words.days);
			format.setDateFormatSymbols(symbols);
		};
		DPGlobal.parseDate = function(date, format, language) {
			if (!date) return undefined;
			if (date instanceof Date) return date;
			var dt = DPGlobal._parseDateDiff(date);
			if (dt) return dt;
			if (typeof format == 'string') {
				format = new JsSimpleDateFormat(format, 'en', true);
				format.isLenient = true;
			}
			DPGlobal.setFormatSymbols(format, language);
			return Datepicker.prototype._local_to_utc(format.parse(date));
		};
		DPGlobal.formatDate = function(date, format, language, first=1) {
			if (!date) return '';
			if (typeof format == 'string') {
				format = new JsSimpleDateFormat(format, language, true);
				format.isLenient = true;
				format.isNetCompat = true;
			}
			DPGlobal.setFormatSymbols(format, language);
			return format.format(Datepicker.prototype._utc_to_local(date),first);
		};
	}else{
	    console.log('  JsSimpleDateFormat:', JsSimpleDateFormat);
	}

	$.fn.datepicker.DPGlobal = DPGlobal;


	/* DATEPICKER NO CONFLICT
	* =================== */

	$.fn.datepicker.noConflict = function(){
		$.fn.datepicker = old;
		return this;
	};

	/* DATEPICKER VERSION
	 * =================== */
	$.fn.datepicker.version = '2.1.0';

	/* DATEPICKER DATA-API
	* ================== */

	$(document).on(
		'focus.datepicker.data-api click.datepicker.data-api',
		'[data-provide="datepicker"]',
		function(e){
            console.log("  !!!!!click on input")
			var $this = $(this);
			if ($this.data('datepicker'))
				return;
			e.preventDefault();
			// component click requires us to explicitly show it
			datepickerPlugin.call($this, 'show');
		}
	);
	$(function(){
        console.log("!!!global function here")
		datepickerPlugin.call($('[data-provide="datepicker-inline"]'));
	});

}));

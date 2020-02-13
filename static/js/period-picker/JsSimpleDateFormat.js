/*! ****
JsSimpleDateFormat v2.0.1 (20160316)
This library is for formatting and parsing date time

Copyright (C) 2008, 2016 AT Mulyana (atmulyana@yahoo.com)

This library is free software; you can redistribute it and/or modify it
under the terms of the GNU Lesser General Public License version 3.0
or later version
See http://gnu.org/licenses/lgpl.html

Send the bug report to 'atmulyana@yahoo.com'
*****/
Function.prototype.__extends__ = function(fParent,oExtMembers) {
	this.prototype = new fParent();
	for (var i = 1; i<arguments.length; i++) {
		for (m in arguments[i]) {
			if (this.prototype[m] !== arguments[i][m]) this.prototype[m] = arguments[i][m];
		}
	}
}

function JsDateFormatSymbols(sLocale) {
	if (!JsDateFormatSymbols.__symbols__[sLocale]) sLocale = 'en';
	var oSymbols = JsDateFormatSymbols.__symbols__[sLocale];
	for (p in oSymbols) {
		var ar = [].concat(oSymbols[p]);
		this._setMap(ar);
		this['_'+p] = ar;
	}
	if (this._amPmStrings) {
		this._shortAmPmStrings = []
		for (var i=0; i<this._amPmStrings.length; i++) this._shortAmPmStrings.push(this._amPmStrings[i].charAt(0));
		this._setMap(this._shortAmPmStrings);
	}
}
JsDateFormatSymbols.prototype = {
_setMap: function(arSymbols) {
	var map = {};
	for (var i=0; i<arSymbols.length; i++) map[arSymbols[i].toUpperCase()] = i;
	arSymbols.__map__ = map;
},
getAmPmStrings: function() {
	return this._amPmStrings;
},
getShortAmPmStrings: function() {
	return this._shortAmPmStrings;
},
getEras: function() {
	return this._eras;
},
getMonths: function() {
	return this._months;
},
getShortMonths: function() {
	return this._shortMonths;
},
getShortWeekdays: function() {
	return this._shortWeekdays;
},
getWeekdays: function() {
	return this._weekdays;
},
setAmPmStrings: function(arAmPmStrings) {
	this._setMap(arAmPmStrings);
	this._amPmStrings = arAmPmStrings;
	this._shortAmPmStrings = []
	for (var i=0; i<this._amPmStrings.length; i++) this._shortAmPmStrings.push(this._amPmStrings[i].charAt(0));
	this._setMap(this._shortAmPmStrings);
},
setEras: function(arEras) {
	this._setMap(arEras);
	this._eras = arEras;
},
setMonths: function(arMonths) {
	this._setMap(arMonths);
	return this._months = arMonths;
},
setShortMonths: function(arShortMonths) {
	this._setMap(arShortMonths);
	return this._shortMonths = arShortMonths;
},
setShortWeekdays: function(arShortWeekdays) {
	this._setMap(arShortWeekdays);
	return this._shortWeekdays = arShortWeekdays;
},
setWeekdays: function(arWeekdays) {
	this._setMap(arWeekdays);
	return this._weekdays = arWeekdays;
}
};
JsDateFormatSymbols.__symbols__ = {
en: {
	amPmStrings: ['AM','PM'],
	eras: ['AD','BC'],
	months: ['January','February','March','April','May','June','July','August','September','October','November','December'],
	shortMonths: ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
	shortWeekdays: ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'],
	weekdays: ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
},
id: {
	amPmStrings: ['AM','PM'],
	eras: ['M','SM'],
	months: ['Januari','Februari','Maret','April','Mei','Juni','Juli','Agustus','September','Oktober','Nopember','Desember'],
	shortMonths: ['Jan','Feb','Mar','Apr','Mei','Jun','Jul','Agu','Sep','Okt','Nop','Des'],
	shortWeekdays: ['Min','Sen','Sel','Rab','Kam','Jum','Sab'],
	weekdays: ['Minggu','Senin','Selasa','Rabu','Kamis','Jumat','Sabtu']
}
};

function JsSimpleDateFormat(sPattern,param,isNetCompat) {
	this._arPtn = [];
	this._ptn = null;
	this.flexWhiteSpace = true;
	this.isLenient = false;
	this.isNetCompat = isNetCompat ? true : false;
	
	if (sPattern) this.applyPattern(sPattern);
	else this.applyPattern(this._getDefaultPattern());
	if (param) {
		if (param instanceof JsDateFormatSymbols) this.setDateFormatSymbols(param);
		else this.setDateFormatSymbols(new JsDateFormatSymbols(param));
	} else {
		this.setDateFormatSymbols(new JsDateFormatSymbols('en'));
	}
	
	var oStDt = new Date();
	try {
		oStDt.setFullYear(oStDt.getFullYear()-80); //See if error prior to 1970 GMT
	} catch (e) {
		oStDt = new Date(0);
	}
	this.set2DigitYearStart(oStDt);
}

(function() {

	function Base() {
	}
	JsSimpleDateFormat._Base = Base;
	Base.prototype = {
		isNumber: function() {
			return false;
		},
		parse: function(s,isNN) {
			return -1;
		},
		toStr: function() {
			return "";
		}
	};

	function Str(sInitVal) {
		Base.call(this);
		this._vals = [];
		if (sInitVal) this.append(sInitVal);
	}
	JsSimpleDateFormat._Str = Str;
	Str.__extends__(Base, {
		flexWhiteSpace: false,
		append: function(s) {
			this._vals.push(s);
		},
		parse: function(s,isNN) {
			var sVal = this.toStr();
			if (this.flexWhiteSpace) {
				var sRe = sVal.replace(/\s+/g," ");
				if (sRe == " ") sRe = "\\s+";
				else sRe = "\\s*" + sRe.replace(/^\s+/,'').replace(/\s+$/,'').replace(/([^a-zA-Z0-9\s])/g,"\\$1").replace(/\s+/g,"\\s+") + "\\s*";
				var reVal = new RegExp("^("+sRe+")");
				if (reVal.test(s)) return RegExp.$1.length;
			} else {
				if (s.indexOf(sVal) == 0) return sVal.length;
			}
			return -1;
		},
		toStr: function() {
			return this._vals.join("");
		}
	});

	function Ltr() {
		Base.call(this);
		this._count = 1;
		this._parseVal = parseInt("NaN");
	}
	JsSimpleDateFormat._Ltr = Ltr;
	Ltr.__extends__(Base, {
		name: "",
		dt: new Date(),
		fmtSb: new JsDateFormatSymbols('en'),
		isNetCompat: false,
		addCount: function() {
			this._count++;
		},
		applyParseValue: function(oDate,oFields) {
			return oDate;
		},
		getParseValue: function() {
			return this._parseVal;
		},
		getValue: function() {
			return -1;
		}
	});

	function Text() {
		Ltr.call(this);
	}
	JsSimpleDateFormat._Text = Text;
	Text.__extends__(Ltr, {
		getIndex: function() {
			return -1;
		},
		getLong: function() {
			var i = this.getIndex(), arVals = this.getLongValues();
			if (i >= 0 && i < arVals.length) return arVals[i];
			return "";
		},
		getLongValues: function() {
			return [];
		},
		getShort: function() {
			var i = this.getIndex(), arVals = this.getShortValues();
			if (i >= 0 && i < arVals.length) return arVals[i];
			return "";
		},
		getShortValues: function() {
			return [];
		},
		getValue: function() {
			return this.getIndex();
		},
		isShort: function() {
			return this._count < 4;
		},
		parse: function(s,isNN) {
			this._parseVal = parseInt("NaN");
			var arLong = this.getLongValues(), arShort = this.getShortValues();
			var re = new RegExp("^("+arLong.join("|")+"|"+arShort.join("|")+")", "i");
			if (!re.test(s)) return -1;
			var sVal = RegExp.$1.toUpperCase();
			if (arLong.__map__[sVal] !== undefined) {
				this._parseVal = arLong.__map__[sVal];
				return sVal.length;
			}
			if (arShort.__map__[sVal] !== undefined) {
				this._parseVal = arShort.__map__[sVal];
				return sVal.length;
			}
		},
		toStr: function() {
			if (this.isShort()) return this.getShort();
			return this.getLong();
		}
	});

	function Number() {
		Ltr.call(this);
	}
	JsSimpleDateFormat._Number = Number;
	Number.__extends__(Ltr, {
		getNumber: function(first) {
			return this.getValue(first);
		},
		isNumber: function() {
			return true;
		},
		isValidVal: function(iVal) {
			return true;
		},
		_getNumberStr: function(s,isNN) {
			var i = 0, c = s.charAt(0), sVal = "";
			if (isNN) while(i < this._count && c >= '0' && c <= '9') {
				sVal += c;
				if (++i < s.length) c = s.charAt(i); else break;
			}
			else while(c >= '0' && c <= '9') { //If next pattern is not number, include all the rest numeric character (this._count is ignored)
				sVal += c;
				if (++i < s.length) c = s.charAt(i); else break;
			}
			return sVal;
		},
		parse: function(s,isNN) {
			this._parseVal = parseInt("NaN");
			var sVal = this._getNumberStr(s,isNN);
			if (sVal.length == 0) return -1;
			var iVal = parseInt(sVal, 10);
			if (this.isValidVal(iVal)) this._parseVal = iVal; else return -1;
			return sVal.length;
		},
		toStr: function(first=0) {
			var sVal = this.getNumber(first)+"", s = "";
			if (sVal.charAt(0) == '-') { sVal = sVal.substr(1); s = "-"; }
			while (sVal.length < this._count) sVal = "0" + sVal;
			return s+sVal;
		}
	});

	function Month() {
		Number.call(this);
		Text.call(this);
	}
	JsSimpleDateFormat._Month = Month;
	Month.__extends__(Number, Text.prototype, {
		name: "month",
		isNumber: function() {
			return this._count < 3;
		},
		isValidVal: function(iVal) {
			return iVal >= 1 && iVal <= 12;
		},
		parse: function(s,isNN) {
			if (this.isNumber()) return Number.prototype.parse.call(this,s,isNN);
			return Text.prototype.parse.call(this,s,isNN);
		},
		toStr: function() {
			if (this.isNumber()) return Number.prototype.toStr.call(this);
			return Text.prototype.toStr.call(this);
		}
	});

	function Year() {
		Number.call(this);
	}
	JsSimpleDateFormat._Year = Year;
	Year.__extends__(Number, {
		name: "year",
		stC: 1900,
		stY: 1970,
		parse: function(s,isNN) {
			var j = 0;
			if (s.charAt(0) == '-') {
				s = s.substr(1);
				j++;
			}
			var i = Number.prototype.parse.call(this,s,isNN);
			if (i == -1) return -1;
			if (j > 0) this._parseVal = -this._parseVal;
			if (this._count < 3/*yy or y*/ && this._parseVal > 0 && i == 2/*exactly 2 digits, not less/more*/) {
				var iY = this.stC + this._parseVal;
				if (iY <= this.stY) iY += 100;
				this._parseVal = iY;
			}
			return i+j;
		},
		toStr: function() {
			if (this._count == 2 || this.isNetCompat && this._count == 1) {
				var sVal = (this.getNumber() % 100) + "";
				if (sVal.length < 2 && this._count == 2) return "0"+sVal;
				return sVal;
			}
			return Number.prototype.toStr.call(this);
		}
	});
	
	var ltr = {};
	JsSimpleDateFormat._ltr = ltr;
	
	ltr.G = function() {
		Text.call(this);
	}
	ltr.G.__extends__(Text, {
		name: "era",
		getIndex: function() {
			return (this.dt.getFullYear() > 0 ? 0 : 1);
		},
		getLongValues: function() {
			return this.fmtSb.getEras();
		},
		getShortValues: function() {
			return this.getLongValues();
		}
	});
	
	ltr.g = function() {
		ltr.G.call(this);
	}
	ltr.g.isNetLetter = true;
	ltr.g.__extends__(ltr.G);
	
	ltr.y = function() {
		Year.call(this);
	}
	ltr.y.__extends__(Year, {
		applyParseValue: function(oDate,oFields) {
			if (oFields.era) {
				if (oFields.era.getParseValue()==0 && this._parseVal<=0) return null;
				if (oFields.era.getParseValue()==1 && this._parseVal>0) this._parseVal = -this._parseVal+1;
			}
			oDate.setFullYear(this._parseVal);
			return oDate;
		},
		getNumber: function() {
			var iVal = this.getValue();
			return (iVal <= 0) ? (-iVal + 1) : iVal;
		},
		getValue: function() {
			return this.dt.getFullYear();
		}
	});
	
	ltr.Y = function() {
		ltr.y.call(this);
	}
	ltr.Y.__extends__(ltr.y, {
		name: "weekYear",
		_getSaturday: function(oDate) {
			return new Date(oDate.getFullYear(), oDate.getMonth(), oDate.getDate() - oDate.getDay() + 6);
		},
		applyParseValue: function(oDate,oFields) {
			if (!oFields["year"]) {
				if (oDate.getMonth() < 11 || oDate.getDate() < 25) oDate.setFullYear(this._parseVal);
				else {
					oDate.setFullYear(this._parseVal - 1);
					var iWY = this._getSaturday(oDate).getFullYear();
					if (iWY < this._parseVal) oDate.setFullYear(this._parseVal);
				}
			}
			return oDate;
		},
		getValue: function() {
			return this._getSaturday(this.dt).getFullYear();
		}
	});
	
	ltr.M = function() {
		Month.call(this);
	}
	ltr.M.__extends__(Month, {
		applyParseValue: function(oDate,oFields) {
			var iVal = this.getParseValue(), iD = oDate.getDate();
			oDate.setMonth(iVal);
			if (iVal < oDate.getMonth()) oDate.setDate(0); //if the day exceeds the last day of the month then set it to the last day
			return oDate;
		},
		getIndex: function() {
			return this.dt.getMonth();
		},
		getLongValues: function() {
			return this.fmtSb.getMonths();
		},
		getNumber: function() {
			return this.dt.getMonth() + 1;
		},
		getParseValue: function() {
			return this.isNumber() ? this._parseVal-1 : this._parseVal;
		},
		getShortValues: function() {
			return this.fmtSb.getShortMonths();
		}
	});
	
	ltr.L = function() {
		ltr.M.call(this);
	}
	ltr.L.__extends__(ltr.M, {
		isNumber: function() {
			return true;
		}
	});
	
	ltr.D = function() {
		Number.call(this);
	}
	ltr.D.__extends__(Number, {
		_ends: [31,28,31,30,31,30,31,31,30,31,30,31],
		name: "dayOfYear",
		_checkLeapYear: function(oDate) {
			//I dont trust year % 4
			var oDt = new Date(oDate.getTime());
			oDt.setDate(1); oDt.setMonth(1); oDt.setDate(29); //Set to Feb 29 of this year if exists
			if (oDt.getDate() == 29) this._ends[1] = 29; else this._ends[1] = 28; //If date doesnt change then Feb 29 of this year exists
		},	
		applyParseValue: function(oDate,oFields) {
			if (oFields.year) if (oFields.year.applyParseValue(oDate,oFields) == null) return null;
			this._checkLeapYear(oDate);
			var arEnds = this._ends, iD = this.getParseValue(), iM = 0;
			while (iD > arEnds[iM] && iM < arEnds.length) iD -= arEnds[iM++];
			if (iM >= arEnds.length) return null;
			oDate.setDate(1);
			oDate.setMonth(iM);
			oDate.setDate(iD);
			return oDate;
		},
		getDay: function() {
			this._checkLeapYear(this.dt);
			var arEnds = this._ends;
			var iMonth = this.dt.getMonth(), iDay = 0;
			for (var i=0; i<iMonth; i++) iDay += arEnds[i];
			return iDay + this.dt.getDate();
		},
		getValue: function() {
			return this.getDay();
		},
		isValidVal: function(iVal) {
			return iVal >= 1 && iVal <= 366;
		}
	});
	
	ltr.E = function() {
		Text.call(this);
	}
	ltr.E.__extends__(Text, {
		name: "dayOfWeek",
		applyParseValue: function(oDate,oFields) {
			oDate.setDate(1);
			oDate.setTime(oDate.getTime() + ((this._parseVal - oDate.getDay() + 7) % 7) * 86400000);
			return oDate;
		},
		getIndex: function() {
			return this.dt.getDay();
		},
		getLongValues: function() {
			return this.fmtSb.getWeekdays();
		},
		getShortValues: function() {
			return this.fmtSb.getShortWeekdays();
		}
	});
	
	ltr.d = function() {
		ltr.D.call(this);
	}
	ltr.d.__extends__(ltr.D, ltr.E.prototype, {
		name: "day",
		addCount: function() {
			Ltr.prototype.addCount.call(this);
			this.name = this.isNumber() ? "day" : ltr.E.prototype.name;
		},
		applyParseValue: function(oDate,oFields) {
			if (!this.isNumber()) return ltr.E.prototype.applyParseValue.call(this,oDate,oFields);
			
			if (oFields.year) if (oFields.year.applyParseValue(oDate,oFields) == null) return null;
			this._checkLeapYear(oDate);
			if (oFields.month) if (oFields.month.applyParseValue(oDate,oFields) == null) return null;
			var arEnds = this._ends, iD = this.getParseValue(), iM = oDate.getMonth();
			if (iD < 1 || iD > arEnds[iM]) return null;
			oDate.setDate(iD);
			return oDate;
		},
		getDay: function() {
			return this.dt.getDate();
		},
		getValue: function() {
			if (this.isNumber()) return ltr.D.prototype.getValue.call(this);
			return ltr.E.prototype.getValue.call(this);
		},
		isNumber: function() {
			return !this.isNetCompat || this._count < 3;
		},
		isValidVal: function(iVal) {
			return iVal >= 1 && iVal <= 31;
		},
		parse: function(s,isNN) {
			if (this.isNumber()) return ltr.D.prototype.parse.call(this,s,isNN);
			return ltr.E.prototype.parse.call(this,s,isNN);
		},
		toStr: function() {
			if (this.isNumber()) return ltr.D.prototype.toStr.call(this);
			return ltr.E.prototype.toStr.call(this);
		}
	});
	
	ltr.w = function() {
		ltr.D.call(this);
	}
	ltr.w.__extends__(ltr.D, {
		name: "weekOfYear",
		_resetMonth: function(oDate) {
			oDate.setMonth(0);
		},
		applyParseValue: function(oDate,oFields) {
			oDate.setDate(1);
			this._resetMonth(oDate);
			oDate.setTime(oDate.getTime() - oDate.getDay()*86400000 + (this._parseVal-1)*7*86400000); //86400000 == ms per day
			return oDate;
		},
		getParseValue: function() {
			return this.getValue();
		},
		getValue: function(first) {
			return this.getWeek(first);
		},
		getWeek: function(first) {
			/*** It's my magic formula for getting the week number. Hope no bug at all. ***/
			/*BUG: when first day is Monday*/
			var iDay = this.getDay();
			var iWeek = Math.ceil(iDay/7);
			iDay = iDay % 7;
			iDay = iDay ? iDay : 7  //if week starts at Monday, iday is 1~7
			if(first == 0){
			    //if week starts at Sunday, iday is 0~6
			    iDay = iDay - 1;
			};
			var calendarDay = this.dt.getDay();
			if(first == 1){
			    // if week starts at Monday, calendarDay is 1~7
			    calendarDay = calendarDay ? calendarDay : 7;
			}
			return ((calendarDay < iDay) ? (iWeek+1) : iWeek);
		},
		isValidVal: function(iVal) {
			return iVal >= 1 && iVal <= 54;
		}
	});
	
	ltr.W = function() {
		ltr.w.call(this);
	}
	ltr.W.__extends__(ltr.w, {
		name: "weekOfMonth",
		_resetMonth: function(oDate) {
		},
		getDay: function() {
			return this.dt.getDate();
		},
		isValidVal: function(iVal) {
			return iVal >= 1 && iVal <= 6;
		}
	});
	
	ltr.F = function() {
		Number.call(this);
	}
	ltr.F.__extends__(Number, {
		name: "dayOfWeekInMonth",
		applyParseValue: function(oDate,oFields) {
			oDate.setDate((this.getParseValue()-1)*7 + 1);
			oDate.setDate(oDate.getDate() + 7 - oDate.getDay());
			return oDate;
		},
		isValidVal: function(iVal) {
			return iVal >= 1 && iVal <= 5;
		},
		getValue: function() {
			return Math.ceil(this.dt.getDate() / 7);
		}
	});
	
	ltr.u = function() {
		Number.call(this);
	}
	ltr.u.__extends__(Number, {
		name: "dayOfWeek",
		applyParseValue: function(oDate,oFields) {
			oDate.setDate(1);
			var iParseVal = this._parseVal;
			if (iParseVal == 7) iParseVal = 0;
			oDate.setTime(oDate.getTime() + ((iParseVal - oDate.getDay() + 7) % 7) * 86400000);
			return oDate;
		},
		getValue: function() {
			var iDay = this.dt.getDay();
			return iDay == 0 ? 7 : iDay;
		},
		isValidVal: function(iVal) {
			return 1 <= iVal && iVal <= 7;
		}
	});
	
	ltr.a = function() {
		Text.call(this);
	}
	ltr.a.__extends__(Text, {
		name: "ampm",
		getIndex: function() {
			return (this.dt.getHours() < 12 ? 0 : 1);
		},
		getLongValues: function() {
			return this.fmtSb.getAmPmStrings();
		},
		getShortValues: function() {
			return this.getLongValues();
		},
		isShort: function() {
			return false;
		}
	});
	
	ltr.t = function() {
		ltr.a.call(this);
	}
	ltr.t.isNetLetter = true;
	ltr.t.__extends__(ltr.a, {
		getShortValues: function() {
			return this.fmtSb.getShortAmPmStrings();
		},
		isShort: function() {
			return this._count == 1;
		}
	});
	
	ltr.H = function() {
		Number.call(this);
	}
	ltr.H.__extends__(Number, {
		name: "hour",
		applyParseValue: function(oDate,oFields) {
			oDate.setHours(this.getParseValue());
			return oDate;
		},
		getValue: function() {
			return this.dt.getHours();
		},
		isValidVal: function(iVal) {
			return iVal >= 0 && iVal <= 23;
		}
	});
	
	ltr.k = function() {
		ltr.H.call(this);
	}
	ltr.k.__extends__(ltr.H, {
		getParseValue: function() {
			return this._parseVal == 24 ? 0 : this._parseVal;
		},
		getNumber: function() {
			var iH = this.dt.getHours();
			return (iH > 0 ? iH : 24);
		},
		isValidVal: function(iVal) {
			return iVal >= 1 && iVal <= 24;
		}
	});
	
	ltr.K = function() {
		Number.call(this);
	}
	ltr.K.__extends__(Number, {
		name: "h12",
		applyParseValue: function(oDate,oFields) {
			var iVal = this.getParseValue();
			if (oFields.ampm && oFields.ampm.getParseValue() == 1) iVal += 12;
			oDate.setHours(iVal);
			return oDate;
		},
		getValue: function() {
			return this.dt.getHours() % 12;
		},
		isValidVal: function(iVal) {
			return iVal >= 0 && iVal <= 11;
		}
	});
	
	ltr.h = function() {
		ltr.K.call(this);
	}
	ltr.h.__extends__(ltr.K, {
		getParseValue: function() {
			return this._parseVal == 12 ? 0 : this._parseVal;
		},
		getNumber: function() {
			var iH = this.dt.getHours() % 12;
			return (iH > 0 ? iH : 12);
		},
		isValidVal: function(iVal) {
			return iVal >= 1 && iVal <= 12;
		}
	});
	
	ltr.m = function() {
		Number.call(this);
	}
	ltr.m.__extends__(Number, {
		name: "minute",
		applyParseValue: function(oDate,oFields) {
			oDate.setMinutes(this.getParseValue());
			return oDate;
		},
		getValue: function() {
			return this.dt.getMinutes();
		},
		isValidVal: function(iVal) {
			return iVal >= 0 && iVal <= 59;
		}
	});
	
	ltr.s = function() {
		Number.call(this);
	}
	ltr.s.__extends__(Number, {
		name: "second",
		applyParseValue: function(oDate,oFields) {
			oDate.setSeconds(this.getParseValue());
			return oDate;
		},
		getValue: function() {
			return this.dt.getSeconds();
		},
		isValidVal: function(iVal) {
			return iVal >= 0 && iVal <= 59;
		}
	});
	
	ltr.S = function() {
		Number.call(this);
	}
	ltr.S.__extends__(Number, {
		name: "ms",
		applyParseValue: function(oDate,oFields) {
			oDate.setMilliseconds(this.getParseValue());
			return oDate;
		},
		getValue: function() {
			return this.dt.getMilliseconds();
		},
		isValidVal: function(iVal) {
			return iVal >= 0 && iVal <= 999;
		}
	});
	
	ltr.f = function() {
		ltr.S.call(this);
	}
	ltr.f.isNetLetter = true;
	ltr.f.__extends__(ltr.S, {
		isValidVal: function(iVal) {
			var sVal = iVal + '';
			if (sVal.length <= 3) return true;
			return sVal.substr(3).replace('0', '') === '';
		},
		parse: function(s,isNN) {
			var sVal = this._getNumberStr(s,isNN);
			if (sVal.length == 0) return -1;
			this._parseVal = parseInt((sVal+"00").substr(0,3));
			return sVal.length;
		},
		toStr: function() {
			var sVal = ("000"+this.getNumber()).substr(-3);
			if (this._count == 1) sVal = sVal.substr(0,1);
			else if (this._count == 2) sVal = sVal.substr(0,2);
			else while (sVal.length < this._count) sVal = sVal + "0";
			return sVal;
		}
	});
	
	ltr.z = function() {
		Text.call(this);
	}
	ltr.z.__extends__(Text, {
		name: "timezone",
		_netRegex: [ /^(\+|-)(\d{1,2})/, /^(\+|-)(\d{2})/, /^(\+|-)(\d{1,2}):(\d{2})/ ],
		_regex: /^(UTC|GMT[^+-]|GMT$)|^(GMT)((\+|-)(\d{1,2}):(\d{2}))|^(\+|-)(\d{2})(\d{2})/i,
		_getTzComp: function() {
			var tzo = this.dt.getTimezoneOffset();
			var arComp = [];
			arComp[0] = tzo > 0 ? "-" : "+";
			tzo = Math.abs(tzo);
			arComp[1] = ("0" + Math.floor(tzo / 60)).substr(-2);
			arComp[2] = ("0" + (tzo % 60)).substr(-2);
			return arComp;
		},
		_setParseValue: function(sSign, sHour, sMinute) {
			this._parseVal = parseInt("NaN");
			var iHour = parseInt(sHour), iMinute = parseInt(sMinute);
			if (iHour > 23 || iMinute > 59) return;
			var iDiff = iHour * 60 + iMinute;
			if (sSign == "-") iDiff = -iDiff;
			if (iDiff < -780 || iDiff > 840) return;
			this._parseVal = iDiff;
		},
		applyParseValue: function(oDate,oFields) {
			var diffTime = (oDate.getTimezoneOffset() + this.getParseValue()) * 60000;
			oDate.setTime(oDate.getTime() - diffTime);
			return oDate;
		},
		getValue: function() {
			return this._parseVal;
		},
		parse: function(s,isNN) {
			var arMatch = this._regex.exec(s);
			var sSign = "+", sHour = "0", sMinute = "0";
			if (arMatch == null) {
				if (this.isNetCompat) {
					arMatch = this._count == 1 ? this._netRegex[0].exec(s)
					        : this._count == 2 ? this._netRegex[1].exec(s)
							: this._netRegex[2].exec(s);
					if (arMatch != null) {
						sSign = arMatch[1];
						sHour = arMatch[2];
						if (arMatch[3]) sMinute = arMatch[3];
						this._setParseValue(sSign, sHour, sMinute);
						if (!isNaN(this._parseVal)) return arMatch[0].length;
					}
				}
				return -1;
			}
			if (arMatch[1]) { //UTC
				this._parseVal = 0;
			} else if (arMatch[2]) { //GMT+/-dd:dd
				if (arMatch[3]) {
					sSign = arMatch[4];
					sHour = arMatch[5];
					sMinute = arMatch[6];
				}
			} else {
				sSign = arMatch[7];
				sHour = arMatch[8];
				sMinute = arMatch[9];
			}
			this._setParseValue(sSign, sHour, sMinute);
			return isNaN(this._parseVal) ? -1 : arMatch[0].length;
		},
		toStr: function() {
			var s = "GMT";
			if (this.dt.getTimezoneOffset() != 0) {
				var arComp = this._getTzComp();
				s += arComp[0] + arComp[1] + ":" + arComp[2];
			}
			return s;
		}
	});
	
	ltr.Z = function() {
		ltr.z.call(this);
	}
	ltr.Z.__extends__(ltr.z, {
		toStr: function() {
			var arComp = this._getTzComp();
			return arComp[0] + arComp[1] + arComp[2];
		}
	});
	
	ltr.X = function() {
		ltr.z.call(this);
	}
	ltr.X.__extends__(ltr.z, {
		_regex: [/^(\+|-)(\d{2})/, /^(\+|-)(\d{2})(\d{2})/, /^(\+|-)(\d{2}):(\d{2})/],
		parse: function(s,isNN) {
			var sSign = "+", sHour = "0", sMinute = "0", arMatch = null;
			if (this._count == 1) {
				arMatch = this._regex[0].exec(s);
			} else if (this._count == 2) {
				arMatch = this._regex[1].exec(s);
			} else {
				arMatch = this._regex[2].exec(s);
			}
			if (arMatch != null) {
				sSign = arMatch[1];
				sHour = arMatch[2];
				sMinute = arMatch[3] || "0";
				this._setParseValue(sSign, sHour, sMinute);
				return arMatch[0].length;
			}
			return -1;
		},
		toStr: function() {
			var arComp = this._getTzComp();
			switch (this._count) {
				case 1: return arComp[0] + arComp[1];
				case 2: return arComp[0] + arComp[1] + arComp[2];
			}
			return arComp[0] + arComp[1] + ":" + arComp[2];
		}
	});
})();

JsSimpleDateFormat.prototype = {
_getDefaultPattern: function() {
	return "dd MMMM yyyy hh:mm a";
},
_getInitDate: function() {
	var oDt = new Date(0);
	oDt.setTime(oDt.getTime() + oDt.getTimezoneOffset()*60000);
	return oDt;
},
applyPattern: function(sPattern) {
	this._arPtn = [];
	var oLtr = JsSimpleDateFormat._ltr;
	var s=new JsSimpleDateFormat._Str(""), c='', oPtn=null, clsPtn, isQ=false, sQ='', i=-1;
	while (++i < sPattern.length) {
		var c1 = sPattern.charAt(i);
		if (c1 == "'") {
			if (i < sPattern.length-1 && sPattern.charAt(i+1) == "'") { //escape a quote by using two quotes which means one quote
				s.append("'");
				i++;
			} else {
				isQ = !isQ;
			}
			c = '';
		} else if (isQ) {
			s.append(c1);
		} else if (c1 == c) {
			oPtn.addCount();
		} else if ((clsPtn = oLtr[c1]) && (!this.isNetCompat && !clsPtn.isNetLetter || this.isNetCompat)) {
			oPtn = new clsPtn();
			if (s.toStr() != "") this._arPtn.push(s);
			s = new JsSimpleDateFormat._Str("");
			this._arPtn.push(oPtn);
			c = c1;
		} else {
			s.append(c1);
			c = '';
		}
	}
	if (s.toStr() != "") this._arPtn.push(s);
	this._ptn = sPattern;
},
format: function(oDate,first=1) {
	JsSimpleDateFormat._Ltr.prototype.isNetCompat = this.isNetCompat;
	JsSimpleDateFormat._Ltr.prototype.fmtSb = this._fmtSb;
	JsSimpleDateFormat._Ltr.prototype.dt = oDate;
	var s = "", arPtn = this._arPtn;
	for (var i=0; i<arPtn.length; i++) s += arPtn[i].toStr(first);
	return s;
},
get2DigitYearStart: function() {
	return this._stDt;
},
getDateFormatSymbols: function() {
	return this._fmtSb;
},
_arFN: ["year","month","dayOfWeek","dayOfWeekInMonth","weekOfMonth","weekOfYear","dayOfYear",
		"day", "weekYear", "hour","h12","minute","second","ms"],
parse: function(s,oPos) {
	JsSimpleDateFormat._Ltr.prototype.isNetCompat = this.isNetCompat;
	JsSimpleDateFormat._Ltr.prototype.fmtSb = this._fmtSb;
	JsSimpleDateFormat._Str.prototype.flexWhiteSpace = this.flexWhiteSpace;
	JsSimpleDateFormat._Year.prototype.stY = this._stY;
	JsSimpleDateFormat._Year.prototype.stC = this._stC;
	
	if (!oPos) oPos = {index:0, errorIndex:-1};
	var i = oPos.index, j = 0, arPtn = this._arPtn, oFields = {};
	while (j < arPtn.length) {
		var oPtn = arPtn[j++];
		var isNN = (j<arPtn.length) ? arPtn[j].isNumber() : false;
		var k = oPtn.parse(s.substr(i),isNN);
		if (k == -1) {
			oPos.errorIndex = i;
			return null;
		}
		
		//Collects all fields inside the parsed string for consistency checks
		if (oPtn instanceof JsSimpleDateFormat._Ltr) { 
			var sFN = oPtn.name;
			if (!this.isLenient && oFields[sFN]/*There has been the field whose the same name*/) {
				if (oFields[sFN].getParseValue() != oPtn.getParseValue()) { //Both fiels must have the same value (consistent)
					oPos.errorIndex = i;
					return null;
				}
			} else {
				oFields[sFN] = oPtn;
			}
		}
		i += k;
	}
	/* At this point, the string matches the pattern */
	
	var oDate = this._getInitDate();
	/* Applies all parsing values to the Date object that will returned */
	for (j=0; j<this._arFN.length; j++) {
		var sFN = this._arFN[j];
		if (oFields[sFN]) if (oFields[sFN].applyParseValue(oDate,oFields) == null) { //Error in applying the parsing value
			oPos.errorIndex = oPos.index + i; //Consider the index after the pattern is the error index
			return null;
		}
	}
	
	JsSimpleDateFormat._Ltr.prototype.dt = oDate; //The date object as the final result
	if (!this.isLenient) {
		/* Checks the consistency between the parsing value (getParseValue) and the final value (getValue) of all fields.
		   The final value becomes different because the later field changes it. */
		for (var sFN in oFields) if (oFields[sFN].getParseValue() != oFields[sFN].getValue()) { //Error if not consistent
			oPos.errorIndex = oPos.index + i; //Consider the index after the pattern is the error index
			return null;
		}
	}
	if (oFields.timezone) oFields.timezone.applyParseValue(oDate,oFields); //timezone must be the last because it can change the other components' values which influences the consistency checking
	
	oPos.index = i;
	return oDate;
},
set2DigitYearStart: function(oStartDate) {
	this._stDt = oStartDate;
	var iY = Math.abs(oStartDate.getFullYear());
	this._stY = iY;
	this._stC = iY - (iY%100);
},
setDateFormatSymbols: function(oFormatSymbols) {
	this._fmtSb = oFormatSymbols;
},
toPattern: function() {
	return this._ptn;
}
};

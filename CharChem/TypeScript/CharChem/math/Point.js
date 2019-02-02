"use strict";
exports.__esModule = true;
// 2D Point (or vector) object
var Point = /** @class */ (function () {
    function Point(x, y) {
        if (x === void 0) { x = 0.0; }
        if (y === void 0) { y = 0.0; }
        this.x = x;
        this.y = y;
    }
    Point.prototype.init = function (newX, newY) {
        this.x = newX;
        this.y = newY;
        return this;
    };
    Point.prototype.fromPoint = function (pt) {
        this.x = pt.x;
        this.y = pt.y;
    };
    Point.prototype.clone = function () {
        return new Point(this.x, this.y);
    };
    Point.is0 = function (a) {
        return Math.abs(a) < 0.001;
    };
    Point.prototype.eq = function (pt) {
        return Point.is0(this.x - pt.x) && Point.is0(this.y - pt.y);
    };
    Point.prototype.iaddn = function (x, y) {
        this.x += x;
        this.y += y;
        return this;
    };
    Point.prototype.iadd = function (pt) {
        this.x += pt.x;
        this.y += pt.y;
        return this;
    };
    Point.prototype.addn = function (x, y) {
        return new Point(this.x + x, this.y + y);
    };
    // Add external point. Point operator + (Point)
    Point.prototype.add = function (pt) {
        return new Point(this.x + pt.x, this.y + pt.y);
    };
    Point.prototype.isubn = function (x, y) {
        this.x -= x;
        this.y -= y;
        return this;
    };
    // subtraction internal (Point)
    Point.prototype.isub = function (pt) {
        this.x -= pt.x;
        this.y -= pt.y;
        return this;
    };
    Point.prototype.subn = function (x, y) {
        return new Point(this.x - x, this.y - y);
    };
    // Point operator - (Point)
    Point.prototype.sub = function (pt) {
        return new Point(this.x - pt.x, this.y - pt.y);
    };
    Point.prototype.neg = function () {
        return new Point(-this.x, -this.y);
    };
    Point.prototype.iminn = function (x1, y1) {
        this.x = Math.min(this.x, x1);
        this.y = Math.min(this.y, y1);
        return this;
    };
    Point.prototype.imin = function (pt) {
        return this.iminn(pt.x, pt.y);
    };
    Point.prototype.imaxn = function (x1, y1) {
        this.x = Math.max(this.x, x1);
        this.y = Math.max(this.y, y1);
        return this;
    };
    Point.prototype.imax = function (pt) {
        return this.imaxn(pt.x, pt.y);
    };
    Point.prototype.ineg = function () {
        this.x = -this.x;
        this.y = -this.y;
        return this;
    };
    // internal multiply by coefficient
    Point.prototype.imul = function (k) {
        this.x *= k;
        this.y *= k;
        return this;
    };
    Point.prototype.mul = function (k) {
        return new Point(this.x * k, this.y * k);
    };
    Point.prototype.rmul = function (k) {
        return new Point(k * this.x, k * this.y);
    };
    Point.prototype.lengthSqr = function () {
        return Math.pow(this.x, 2) + Math.pow(this.y, 2);
    };
    Point.prototype.length = function () {
        return Math.sqrt(this.lengthSqr());
    };
    Point.prototype.distSqrn = function (x1, y1) {
        return Math.pow((this.x - x1), 2) + Math.pow((this.y - y1), 2);
    };
    Point.prototype.distSqr = function (pt) {
        return this.distSqrn(pt.x, pt.y);
    };
    Point.prototype.dist = function (pt) {
        return Math.sqrt(this.distSqr(pt));
    };
    Point.prototype.fromRad = function (radAngle) {
        this.x = Math.cos(radAngle);
        this.y = Math.sin(radAngle);
        return this;
    };
    Point.prototype.fromDeg = function (degAngle) {
        return this.fromRad(degAngle * 0.017453292519943295);
    };
    Point.prototype.itranspose = function () {
        var tmp = this.x;
        this.x = this.y;
        this.y = tmp;
        return this;
    };
    Point.prototype.transpose = function () {
        return new Point(this.y, this.x);
    };
    Point.toa = function (value) {
        return String(Math.round(value * 1000) / 1000);
    };
    Point.prototype.toString = function () {
        return '(' + Point.toa(this.x) + ', ' + Point.toa(this.y) + ')';
    };
    Point.prototype.polarAngle = function () {
        if (this.x === 0) {
            if (this.y === 0) {
                return 0;
            }
            return this.y > 0 ? Math.PI / 2 : -Math.PI / 2;
        }
        return Math.atan2(this.y, this.x);
    };
    return Point;
}());
exports.Point = Point;

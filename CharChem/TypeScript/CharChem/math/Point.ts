// 2D Point (or vector) object
export class Point {
	public type Value = number;
	public x: Value;
	public y: Value;
	public constructor(x: Value = 0.0, y: Value = 0.0) {
		this.x = x;
		this.y = y;
	}
	public init(newX: Value, newY: Value): Point {
		this.x = newX;
		this.y = newY;
		return this;
	}
	public fromPoint(pt: Point) {
		this.x = pt.x;
		this.y = pt.y;
	}
	public clone(): Point {
		return new Point(this.x, this.y);
	}
	public static is0(a: Value): boolean {
		return Math.abs(a) < 0.001;
	}
	public eq(pt: Point): boolean {
		return Point.is0(this.x - pt.x) && Point.is0(this.y - pt.y);
	}
	public iaddn(x: Value, y: Value): Point {
		this.x += x;
		this.y += y;
		return this;
	}
	public iadd(pt: Point): Point {
		this.x += pt.x;
		this.y += pt.y;
		return this;
	}
	public addn(x: Value, y: Value): Point {
		return new Point(this.x + x, this.y + y);
	}
	// Add external point. Point operator + (Point)
	public add(pt: Point): Point {
		return new Point(this.x + pt.x, this.y + pt.y);
	}
	public isubn(x: Value, y: Value): Point {
		this.x -= x;
		this.y -= y;
		return this;
	}
	// subtraction internal (Point)
	public isub(pt: Point): Point {
		this.x -= pt.x;
		this.y -= pt.y;
		return this;
	}
	public subn(x: Value, y: Value): Point {
		return new Point(this.x - x, this.y - y);
	}

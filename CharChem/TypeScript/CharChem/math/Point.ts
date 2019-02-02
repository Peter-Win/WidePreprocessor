// 2D Point (or vector) object
export class Point {
	public x: number;
	public y: number;
	public constructor(x: number = 0.0, y: number = 0.0) {
		this.x = x;
		this.y = y;
	}
	public init(newX: number, newY: number): Point {
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
	public static is0(a: number): boolean {
		return Math.abs(a) < 0.001;
	}
	public eq(pt: Point): boolean {
		return Point.is0(this.x - pt.x) && Point.is0(this.y - pt.y);
	}
	public iaddn(x: number, y: number): Point {
		this.x += x;
		this.y += y;
		return this;
	}
	public iadd(pt: Point): Point {
		this.x += pt.x;
		this.y += pt.y;
		return this;
	}
	public addn(x: number, y: number): Point {
		return new Point(this.x + x, this.y + y);
	}
	// Add external point. Point operator + (Point)
	public add(pt: Point): Point {
		return new Point(this.x + pt.x, this.y + pt.y);
	}
	public isubn(x: number, y: number): Point {
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
	public subn(x: number, y: number): Point {
		return new Point(this.x - x, this.y - y);
	}
	// Point operator - (Point)
	public sub(pt: Point): Point {
		return new Point(this.x - pt.x, this.y - pt.y);
	}
	public neg(): Point {
		return new Point(-this.x, -this.y);
	}
	public iminn(x1: number, y1: number): Point {
		this.x = Math.min(this.x, x1);
		this.y = Math.min(this.y, y1);
		return this;
	}
	public imin(pt: Point): Point {
		return this.iminn(pt.x, pt.y);
	}
	public imaxn(x1: number, y1: number): Point {
		this.x = Math.max(this.x, x1);
		this.y = Math.max(this.y, y1);
		return this;
	}
	public imax(pt: Point): Point {
		return this.imaxn(pt.x, pt.y);
	}
	public ineg(): Point {
		this.x = -this.x;
		this.y = -this.y;
		return this;
	}
	// internal multiply by coefficient
	public imul(k: number): Point {
		this.x *= k;
		this.y *= k;
		return this;
	}
	public mul(k: number): Point {
		return new Point(this.x * k, this.y * k);
	}
	public rmul(k: number): Point {
		return new Point(k * this.x, k * this.y);
	}
	public lengthSqr(): number {
		return this.x ** 2 + this.y ** 2;
	}
	public length(): number {
		return Math.sqrt(this.lengthSqr());
	}
	public distSqrn(x1: number, y1: number): number {
		return (this.x - x1) ** 2 + (this.y - y1) ** 2;
	}
	public distSqr(pt: Point): number {
		return this.distSqrn(pt.x, pt.y);
	}
	public dist(pt: Point): number {
		return Math.sqrt(this.distSqr(pt));
	}
	public fromRad(radAngle: number): Point {
		this.x = Math.cos(radAngle);
		this.y = Math.sin(radAngle);
		return this;
	}
	public fromDeg(degAngle: number): Point {
		return this.fromRad(degAngle * 0.017453292519943295);
	}
	public itranspose(): Point {
		let tmp: number = this.x;
		this.x = this.y;
		this.y = tmp;
		return this;
	}
	public transpose(): Point {
		return new Point(this.y, this.x);
	}
	public static toa(value: number): string {
		return String(Math.round(value * 1000) / 1000);
	}
	public toString(): string {
		return '(' + Point.toa(this.x) + ', ' + Point.toa(this.y) + ')';
	}
	public polarAngle(): number {
		if (this.x === 0) {
			if (this.y === 0) {
				return 0;
			}
			return this.y > 0 ? Math.PI / 2 : -Math.PI / 2;
		}
		return Math.atan2(this.y, this.x);
	}
}


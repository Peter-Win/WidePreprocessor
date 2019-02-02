// Rectangle object
export class Rect {
	public A: Point;
	public B: Point;
	public init(xa: number, ya: number, xb: number, yb: number) {
		this.A.init(xa, ya);
		this.B.init(xb, yb);
	}
}


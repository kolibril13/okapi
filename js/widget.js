import "./widget.css";
import p5 from "p5";

function render({ model, el }) {
	new p5((p) => {
		p.setup = () => {
			p.createCanvas(600, 400, p.WEBGL);
		};

		p.draw = () => {
			p.background(200);
			p.translate(0, 0, 0);
			p.fill(255, 165, 0);
			p.sphere(model.get("radius")); 
			
		};
	}, el);
}
export default { render };
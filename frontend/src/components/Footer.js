import { Toolbar } from "@material-ui/core";

function Footer(props) {

  return (
    <div>

      <div>
        <p>{"Click "}
          <a href="https://github.com/sertman1/www.lovelylatin.com">here</a> for source code.
        </p>
        <p>{"A special thanks to "}
          <a href="https://unimorph.github.io/"> Unimorph</a>
          {" and "} <a href="https://www.thelatinlibrary.com/"> The Latin Library</a>.
        </p>
      </div>

      <div
        style={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
        }}
      >

        <Toolbar style={{ position: "static" }}> <p>Made with 🌈 🍀 ✨ in Charm City</p> </Toolbar>

      </div>

    </div>
  )
}

export default Footer;
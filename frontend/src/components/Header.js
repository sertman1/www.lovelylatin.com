import Image from "./Image.js";
import RomeLandscape from "../images/rome_landscape.jpeg";

function Header(props) {
  return (
    <div>

      <Image src={RomeLandscape} alt="Ancient Rome" link="https://www.museodelprado.es/en/the-collection/art-work/landscape-with-psyche-and-jupiter/191cc2c4-2562-47bd-89aa-97cbf65c6bd7"/>
      
      <div
        style={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
        }}
      >
        <p>"<i>Si hortum in bibliotheca habes, deerit nihil</i>" - Marcus Tullius Cicero</p>
      
      </div>

    </div>
  )
}

export default Header;
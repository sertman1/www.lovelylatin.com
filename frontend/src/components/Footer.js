function Footer(props) {

  return (
    <div>

      <div>
        <p>{"Click "}
          <a href="https://github.com/sertman1/www.lovelylatin.com">here</a> for source code.
        </p>
        <p>{"A special thanks to "}
          <a href="https://www.thelatinlibrary.com/"> The Latin Library</a>
          {" and to "} <a href="https://latin-words.com/">William Whitaker's Words</a>.
        </p>
      </div>

      <div
        style={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
        }}
      >
        <p>Made with 🌈 🍀 ✨ in Charm City</p>

      </div>

    </div>
  )
}

export default Footer;
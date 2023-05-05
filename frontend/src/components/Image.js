function Image(props) {
  const { imgsrc, alt, link } = props;

  return (
    <div>
      <div
        style={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
        }}
      >
        <img
          src={imgsrc} alt={alt}
          style={{ width: "59.2592592593vh", height: "28vh" }}
          onClick={() => window.open(link)}
        />
      </div>
    </div>
  );
}

export default Image;
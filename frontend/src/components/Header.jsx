import {useState} from 'react'
import { Link, useNavigate, useMatch, useResolvedPath } from 'react-router-dom'
import "../styles/Header.css"

const Header = () => {
  const {isLoggedIn, setIsLoggedIn} = useState("");
  const navigate = useNavigate();

  const handleLogout = () =>{
    localStorage.removeItem(ACCESS_TOKEN)
    localStorage.removeItem(REFRESH_TOKEN)
    setIsLoggedIn(false)
    navigate('/login')
  }
  return (
    <>
        <nav className='nav'>
            <Link className="site-title" to="/">Project Management</Link>


            <div>
              {isLoggedIn ? (
                <ul>
                    <Link text='Home' url="/home" />
                    <button onClick={handleLogout}>Logout</button>
                </ul>
              ) : (
                <ul>
                    <CustomLink to="/login">Login</CustomLink>
                    <CustomLink to="/register">Register</CustomLink>
                </ul>
              )}
                
            </div>
        </nav>
    </>
  )
}

function CustomLink({ to, children, ...props }) {
    const resolvedPath = useResolvedPath(to)
    const isActive = useMatch({ path: resolvedPath.pathname, end: true})

    return (
        <li className={isActive ? "active": ""}>
            <Link to={to} {...props}>{children}</Link>
        </li>
    )
}

export default Header
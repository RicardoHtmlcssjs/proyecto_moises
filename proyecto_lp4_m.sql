-- phpMyAdmin SQL Dump
-- version 4.8.5
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 30-10-2023 a las 11:50:15
-- Versión del servidor: 10.1.38-MariaDB
-- Versión de PHP: 7.3.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `proyecto_lp4_m`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `alumnos`
--

CREATE TABLE `alumnos` (
  `id_alumno` int(11) NOT NULL,
  `nombre` varchar(80) NOT NULL,
  `cedula` int(12) NOT NULL,
  `fec_nac` date NOT NULL,
  `id_carrera` int(11) NOT NULL,
  `id_semestre` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `alumnos`
--

INSERT INTO `alumnos` (`id_alumno`, `nombre`, `cedula`, `fec_nac`, `id_carrera`, `id_semestre`) VALUES
(1, 'Moises Yanez', 78456932, '2003-10-08', 1, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `carrera`
--

CREATE TABLE `carrera` (
  `id_carrera` int(11) NOT NULL,
  `descripcion` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `carrera`
--

INSERT INTO `carrera` (`id_carrera`, `descripcion`) VALUES
(1, 'Informatica'),
(2, 'administracion'),
(4, 'publicidad');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `materias`
--

CREATE TABLE `materias` (
  `id_materia` int(11) NOT NULL,
  `descripcion` varchar(100) NOT NULL,
  `id_carrera` int(11) NOT NULL,
  `id_semestre` int(11) NOT NULL,
  `id_profesor` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `materias`
--

INSERT INTO `materias` (`id_materia`, `descripcion`, `id_carrera`, `id_semestre`, `id_profesor`) VALUES
(1, 'algoritmo', 1, 1, 5),
(2, 'programacion 1', 1, 1, 4),
(3, 'matematica 1', 1, 1, 9);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `notas_alumnos`
--

CREATE TABLE `notas_alumnos` (
  `id_not_alm` int(11) NOT NULL,
  `id_profesor` int(11) NOT NULL,
  `id_alumno` int(11) NOT NULL,
  `id_carrera` int(11) NOT NULL,
  `id_semestre` int(11) NOT NULL,
  `id_materia` int(11) NOT NULL,
  `nota1` double NOT NULL,
  `nota2` double NOT NULL,
  `nota3` double NOT NULL,
  `nota_f` double NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `roles`
--

CREATE TABLE `roles` (
  `id_role` int(11) NOT NULL,
  `descripcion` varchar(80) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `roles`
--

INSERT INTO `roles` (`id_role`, `descripcion`) VALUES
(1, 'administrador'),
(2, 'profesor');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `semestre`
--

CREATE TABLE `semestre` (
  `id_semestre` int(11) NOT NULL,
  `descripcion` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `semestre`
--

INSERT INTO `semestre` (`id_semestre`, `descripcion`) VALUES
(1, '1'),
(2, '2'),
(3, '3'),
(4, '4'),
(5, '5'),
(6, '6'),
(7, '7');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id_usuario` int(11) NOT NULL,
  `usuario` varchar(60) NOT NULL,
  `contrasena` varchar(255) NOT NULL,
  `email` varchar(60) NOT NULL,
  `id_role` int(11) NOT NULL,
  `nombre` varchar(80) NOT NULL,
  `ci` int(12) NOT NULL,
  `fec_hor_reg` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id_usuario`, `usuario`, `contrasena`, `email`, `id_role`, `nombre`, `ci`, `fec_hor_reg`) VALUES
(3, 'administrador', 'administrador', 'administrador@gmail.com', 1, 'admin', 24569200, '2023-10-27 15:52:00'),
(4, 'carrasquel', 'carrasquel', 'manuel@gmail.com', 2, 'Manuel carrasquel', 489621456, '2023-10-18 10:50:00'),
(5, 'damaris1', 'damaris123', 'damaris99@gmail.com', 2, 'Damaris Linarez', 458212222, '2023-10-28 14:40:47'),
(9, 'vicky1234', 'vicjy1234', 'vicky@gmail.com', 2, 'Vicky Linarez', 65767567, '2023-10-28 14:54:09'),
(11, 'uzuamki', 'uzumaki123', 'uzumaki@gmail.com', 2, 'Naruto Uzumaki', 457896526, '2023-10-28 18:17:37'),
(12, 'retali', 'retali123', 'retali@gmail.com', 2, 'Angel Retali', 2147483647, '2023-10-28 18:42:56');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `alumnos`
--
ALTER TABLE `alumnos`
  ADD PRIMARY KEY (`id_alumno`),
  ADD KEY `fk_id_carrera` (`id_carrera`),
  ADD KEY `fk_semestre` (`id_semestre`);

--
-- Indices de la tabla `carrera`
--
ALTER TABLE `carrera`
  ADD PRIMARY KEY (`id_carrera`);

--
-- Indices de la tabla `materias`
--
ALTER TABLE `materias`
  ADD PRIMARY KEY (`id_materia`),
  ADD KEY `fk_id_carrera` (`id_carrera`),
  ADD KEY `fk_id_semestre` (`id_semestre`),
  ADD KEY `fk_id_profesor` (`id_profesor`);

--
-- Indices de la tabla `notas_alumnos`
--
ALTER TABLE `notas_alumnos`
  ADD PRIMARY KEY (`id_not_alm`),
  ADD KEY `fk_id_profesor` (`id_profesor`),
  ADD KEY `fk_id_carrera` (`id_carrera`),
  ADD KEY `fk_id_alumno` (`id_alumno`),
  ADD KEY `fk_id_semestre` (`id_semestre`),
  ADD KEY `fk_id_materia` (`id_materia`);

--
-- Indices de la tabla `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`id_role`);

--
-- Indices de la tabla `semestre`
--
ALTER TABLE `semestre`
  ADD PRIMARY KEY (`id_semestre`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id_usuario`),
  ADD KEY `fk_id_roles` (`id_role`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `alumnos`
--
ALTER TABLE `alumnos`
  MODIFY `id_alumno` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `carrera`
--
ALTER TABLE `carrera`
  MODIFY `id_carrera` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `materias`
--
ALTER TABLE `materias`
  MODIFY `id_materia` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `notas_alumnos`
--
ALTER TABLE `notas_alumnos`
  MODIFY `id_not_alm` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `roles`
--
ALTER TABLE `roles`
  MODIFY `id_role` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `semestre`
--
ALTER TABLE `semestre`
  MODIFY `id_semestre` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `alumnos`
--
ALTER TABLE `alumnos`
  ADD CONSTRAINT `alumnos_ibfk_2` FOREIGN KEY (`id_semestre`) REFERENCES `semestre` (`id_semestre`),
  ADD CONSTRAINT `alumnos_ibfk_3` FOREIGN KEY (`id_carrera`) REFERENCES `carrera` (`id_carrera`);

--
-- Filtros para la tabla `materias`
--
ALTER TABLE `materias`
  ADD CONSTRAINT `materias_ibfk_2` FOREIGN KEY (`id_carrera`) REFERENCES `carrera` (`id_carrera`),
  ADD CONSTRAINT `materias_ibfk_3` FOREIGN KEY (`id_semestre`) REFERENCES `semestre` (`id_semestre`);

--
-- Filtros para la tabla `notas_alumnos`
--
ALTER TABLE `notas_alumnos`
  ADD CONSTRAINT `notas_alumnos_ibfk_1` FOREIGN KEY (`id_alumno`) REFERENCES `alumnos` (`id_alumno`),
  ADD CONSTRAINT `notas_alumnos_ibfk_2` FOREIGN KEY (`id_profesor`) REFERENCES `usuarios` (`id_usuario`),
  ADD CONSTRAINT `notas_alumnos_ibfk_3` FOREIGN KEY (`id_materia`) REFERENCES `materias` (`id_materia`),
  ADD CONSTRAINT `notas_alumnos_ibfk_4` FOREIGN KEY (`id_carrera`) REFERENCES `carrera` (`id_carrera`),
  ADD CONSTRAINT `notas_alumnos_ibfk_5` FOREIGN KEY (`id_semestre`) REFERENCES `semestre` (`id_semestre`);

--
-- Filtros para la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD CONSTRAINT `usuarios_ibfk_1` FOREIGN KEY (`id_role`) REFERENCES `roles` (`id_role`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

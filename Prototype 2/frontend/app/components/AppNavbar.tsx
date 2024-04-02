"use client"
import {Avatar, Button, Navbar, NavbarBrand, NavbarContent, NavbarItem} from "@nextui-org/react";
import {Link} from "@nextui-org/link";
import Image from "next/image";

export default function AppNavbar() {
    return (
        <Navbar shouldHideOnScroll className={"bg-background dark"}>
            <NavbarBrand>
                <Image src={"/DVerse_logo.png"} alt={"DVerse"} height={25} width={25}/>
                <p className="font-bold text-inherit ml-4">DVerse</p>
            </NavbarBrand>
            <NavbarContent className="hidden sm:flex gap-4" justify="center">
                <NavbarItem isActive>
                    <Link href="#">
                        Chat
                    </Link>
                </NavbarItem>
                <NavbarItem>
                    <Link color="foreground" href="#" aria-current="page">
                        Explore
                    </Link>
                </NavbarItem>
                <NavbarItem>
                    <Link color="foreground" href="#">
                        Contact
                    </Link>
                </NavbarItem>
            </NavbarContent>
            <NavbarContent justify="end">
                <Avatar>

                </Avatar>
            </NavbarContent>
        </Navbar>
    )
}
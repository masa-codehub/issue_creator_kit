workspace "Issue Creator Kit" {
    model {
        # 1. Actors (Context Layer)
        !include context/people.dsl

        # 2. Systems & Boundaries (Context Layer)
        !include context/system-context.dsl

        # 3. Containers (Container Layer)
        # Extend the 'ick' system defined in system-context.dsl
        extend ick {
            !include container/container-diagram.dsl
        }

        # 4. Components (Component Layer)
        !include component/cli-components.dsl
        !include component/usecase-components.dsl
        !include component/domain-components.dsl
        !include component/infra-components.dsl
    }

    views {
        systemContext ick "SystemContext" {
            include *
            autoLayout lr
        }

        container ick "ContainerView" {
            include *
            autoLayout lr
        }

        component cli "CLI_ComponentView" {
            include *
            autoLayout lr
        }

        component usecase "UseCase_ComponentView" {
            include *
            autoLayout lr
        }

        component domain "Domain_ComponentView" {
            include *
            autoLayout lr
        }

        component infra "Infrastructure_ComponentView" {
            include *
            autoLayout lr
        }

        styles {
            element "External" {
                background #999999
                color #ffffff
            }
            element "Software System" {
                background #1168bd
                color #ffffff
            }
            element "Container" {
                background #438dd5
                color #ffffff
            }
            element "Person" {
                shape Person
                background #08427b
                color #ffffff
            }
        }
    }

    !docs docs/
}

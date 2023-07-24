import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.jupiter.MockitoExtension;
import org.junit.jupiter.api.extension.ExtendWith;
import static org.junit.jupiter.api.Assertions.*;
import org.apache.fineract.useradministration.service.AppUserReadPlatformServiceImpl;
import org.springframework.jdbc.core.JdbcTemplate;

@ExtendWith(MockitoExtension.class)
public class AppUserReadPlatformServiceImplTest {

    @InjectMocks
    private AppUserReadPlatformServiceImpl appUserReadPlatformService;

    @Mock
    private JdbcTemplate jdbcTemplate;

    @Test
    public void testIsUsernameExistWithExistingUsername() {
        String username = "existingUser";
        Mockito.when(jdbcTemplate.queryForObject(Mockito.anyString(), Mockito.eq(Integer.class), Mockito.any())).thenReturn(1);
        boolean result = appUserReadPlatformService.isUsernameExist(username);
        assertTrue(result);
    }

    @Test
    public void testIsUsernameExistWithNonExistingUsername() {
        String username = "nonExistingUser";
        Mockito.when(jdbcTemplate.queryForObject(Mockito.anyString(), Mockito.eq(Integer.class), Mockito.any())).thenReturn(0);
        boolean result = appUserReadPlatformService.isUsernameExist(username);
        assertFalse(result);
    }

    @Test
    public void testIsUsernameExistWithNullUsername() {
        String username = null;
        Mockito.when(jdbcTemplate.queryForObject(Mockito.anyString(), Mockito.eq(Integer.class), Mockito.any())).thenReturn(0);
        boolean result = appUserReadPlatformService.isUsernameExist(username);
        assertFalse(result);
    }
}

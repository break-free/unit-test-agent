import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.jupiter.MockitoExtension;
import org.junit.jupiter.api.extension.ExtendWith;
import static org.junit.jupiter.api.Assertions.*;
import org.apache.fineract.portfolio.self.loanaccount.service.AppuserLoansMapperReadServiceImpl;
import org.springframework.jdbc.core.JdbcTemplate;

@ExtendWith(MockitoExtension.class)
public class AppuserLoansMapperReadServiceImplTest {

    @InjectMocks
    private AppuserLoansMapperReadServiceImpl appuserLoansMapperReadService;

    @Mock
    private JdbcTemplate jdbcTemplate;

    @Test
    public void testIsLoanMappedToUserWithValidIds() {
        Long loanId = 1L;
        Long appUserId = 1L;
        Mockito.when(jdbcTemplate.queryForObject(Mockito.anyString(), Mockito.eq(Boolean.class), Mockito.eq(loanId), Mockito.eq(appUserId))).thenReturn(true);
        Boolean result = appuserLoansMapperReadService.isLoanMappedToUser(loanId, appUserId);
        assertTrue(result);
    }

    @Test
    public void testIsLoanMappedToUserWithInvalidIds() {
        Long loanId = -1L;
        Long appUserId = -1L;
        Mockito.when(jdbcTemplate.queryForObject(Mockito.anyString(), Mockito.eq(Boolean.class), Mockito.eq(loanId), Mockito.eq(appUserId))).thenReturn(false);
        Boolean result = appuserLoansMapperReadService.isLoanMappedToUser(loanId, appUserId);
        assertFalse(result);
    }

    @Test
    public void testIsLoanMappedToUserWithNullIds() {
        Long loanId = null;
        Long appUserId = null;
        Mockito.when(jdbcTemplate.queryForObject(Mockito.anyString(), Mockito.eq(Boolean.class), Mockito.eq(loanId), Mockito.eq(appUserId))).thenReturn(false);
        Boolean result = appuserLoansMapperReadService.isLoanMappedToUser(loanId, appUserId);
        assertFalse(result);
    }
}